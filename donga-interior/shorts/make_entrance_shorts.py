from __future__ import annotations

import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent
BLOG = ROOT.parent / "blog"
FFMPEG = ROOT / "_video_deps" / "imageio_ffmpeg" / "binaries" / "ffmpeg-win-x86_64-v7.1.exe"
OUTPUT = ROOT / "sejong-entrance-bench-middle-door-shorts.mp4"
POSTER = ROOT / "sejong-entrance-bench-middle-door-poster.jpg"

WIDTH = 720
HEIGHT = 1280
FPS = 24

SCENES = [
    ("새 폴더 (3)/IMG_9330.JPG", "집의 첫인상,", "현관부터 편안하게", "현관 인테리어", 2.3),
    ("새 폴더 (3)/IMG_9331.JPG", "앉아서 신발 신는", "현관 벤치 포인트", "현관 벤치", 2.4),
    ("새 폴더 (3)/IMG_9326.JPG", "우드톤 중문으로", "거실과 자연스럽게 연결", "중문", 2.3),
    ("새 폴더 (3)/IMG_9327.JPG", "좁은 입구도", "따뜻하고 단정하게", "첫인상", 2.3),
    ("새 폴더 (3)/IMG_9309.JPG", "구축 아파트 현관도", "이렇게 달라집니다", "세종인테리어", 2.5),
    ("새 폴더 (3)/IMG_9334.JPG", "구축 아파트 인테리어", "세종인테리어와 함께하세요!", "SEJONG", 2.7),
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "malgunbd.ttf" if bold else "malgun.ttf"
    path = Path("C:/Windows/Fonts") / name
    if path.exists():
        return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


TAG_FONT = font(20, True)
TITLE_FONT = font(60, True)
SUB_FONT = font(38)


def ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) * (1 - t)


def load(src: str) -> Image.Image:
    return ImageOps.exif_transpose(Image.open(BLOG / src)).convert("RGB")


def cover(img: Image.Image, p: float) -> Image.Image:
    img = ImageEnhance.Color(img).enhance(1.04)
    img = ImageEnhance.Contrast(img).enhance(1.05)
    ratio = img.width / img.height
    canvas_ratio = WIDTH / HEIGHT
    if ratio > canvas_ratio:
        h = HEIGHT
        w = int(h * ratio)
    else:
        w = WIDTH
        h = int(w / ratio)
    zoom = 1.035 + ease(p) * 0.045
    resized = img.resize((int(w * zoom), int(h * zoom)), Image.Resampling.LANCZOS)
    x = (resized.width - WIDTH) // 2 + int(math.sin(p * math.pi) * 14)
    y = (resized.height - HEIGHT) // 2 + int((p - 0.5) * 24)
    x = max(0, min(x, resized.width - WIDTH))
    y = max(0, min(y, resized.height - HEIGHT))
    return resized.crop((x, y, x + WIDTH, y + HEIGHT))


def gradient() -> Image.Image:
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for y in range(HEIGHT):
        if y < HEIGHT * 0.25:
            a = int(90 * (1 - y / (HEIGHT * 0.25)))
        elif y > HEIGHT * 0.35:
            a = int(210 * ((y - HEIGHT * 0.35) / (HEIGHT * 0.65)) ** 1.45)
        else:
            a = 0
        draw.line((0, y, WIDTH, y), fill=(0, 0, 0, max(0, min(210, a))))
    return overlay


OVERLAY = gradient()


def wrap(draw: ImageDraw.ImageDraw, text: str, font_obj: ImageFont.FreeTypeFont, width: int) -> list[str]:
    words = text.split(" ")
    lines: list[str] = []
    line = ""
    for word in words:
        test = f"{line} {word}".strip()
        if draw.textlength(test, font=font_obj) > width and line:
            lines.append(line)
            line = word
        else:
            line = test
    if line:
        lines.append(line)
    return lines


def draw_frame(img: Image.Image, scene: tuple[str, str, str, str, float], p: float, total_p: float) -> Image.Image:
    _, title, sub, tag, _ = scene
    frame = Image.alpha_composite(cover(img, p).convert("RGBA"), OVERLAY)
    draw = ImageDraw.Draw(frame)
    appear = ease(min(1.0, p / 0.2))
    alpha = int(255 * appear)
    shift = int((1 - appear) * 30)
    left = 52
    y = 900 + shift

    draw.rounded_rectangle((left, 106 + shift, left + 220, 148 + shift), radius=21, fill=(205, 166, 102, int(alpha * 0.96)))
    draw.text((left + 20, 127 + shift), tag, font=TAG_FONT, fill=(18, 15, 10, alpha), anchor="lm")

    for line in wrap(draw, title, TITLE_FONT, WIDTH - left * 2)[:2]:
        draw.text((left + 2, y + 2), line, font=TITLE_FONT, fill=(0, 0, 0, int(alpha * 0.35)))
        draw.text((left, y), line, font=TITLE_FONT, fill=(255, 250, 240, alpha))
        y += 72

    y += 14
    for line in wrap(draw, sub, SUB_FONT, WIDTH - left * 2)[:2]:
        draw.text((left, y), line, font=SUB_FONT, fill=(255, 255, 255, int(alpha * 0.92)))
        y += 52

    draw.rounded_rectangle((52, HEIGHT - 70, WIDTH - 52, HEIGHT - 66), radius=2, fill=(255, 255, 255, 65))
    draw.rounded_rectangle((52, HEIGHT - 70, 52 + int((WIDTH - 104) * total_p), HEIGHT - 66), radius=2, fill=(205, 166, 102, 230))
    return frame.convert("RGB")


def main() -> None:
    if not FFMPEG.exists():
        raise FileNotFoundError(f"ffmpeg not found: {FFMPEG}")

    assets = [load(scene[0]) for scene in SCENES]
    total = sum(scene[4] for scene in SCENES)
    draw_frame(assets[0], SCENES[0], 0, 0).save(POSTER, quality=92)

    cmd = [
        str(FFMPEG), "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-pix_fmt", "rgb24",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-r", str(FPS),
        "-i", "-",
        "-an",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-crf", "21",
        str(OUTPUT),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    assert proc.stdin is not None
    elapsed = 0.0
    for idx, scene in enumerate(SCENES):
        frames = max(1, round(scene[4] * FPS))
        for n in range(frames):
            p = n / max(1, frames - 1)
            proc.stdin.write(draw_frame(assets[idx], scene, p, elapsed / total).tobytes())
            elapsed += 1 / FPS
    proc.stdin.close()
    code = proc.wait()
    if code:
        raise RuntimeError(f"ffmpeg failed: {code}")
    print(f"created={OUTPUT}")
    print(f"poster={POSTER}")
    print(f"duration={total:.1f}s size={WIDTH}x{HEIGHT} fps={FPS}")


if __name__ == "__main__":
    main()
