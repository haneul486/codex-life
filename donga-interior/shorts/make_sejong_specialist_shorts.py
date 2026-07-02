from __future__ import annotations

import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent
BLOG = ROOT.parent / "blog"
FFMPEG = ROOT / "_video_deps" / "imageio_ffmpeg" / "binaries" / "ffmpeg-win-x86_64-v7.1.exe"
OUTPUT = ROOT / "sejong-built-apartment-interior-specialist-shorts.mp4"
POSTER = ROOT / "sejong-built-apartment-interior-specialist-poster.jpg"

WIDTH = 720
HEIGHT = 1280
FPS = 24

SCENES = [
    ("새 폴더 (3)/IMG_9322.JPG", "구축 아파트,", "어디까지 바뀔 수 있을까요?", "완성 거실", 3.2),
    ("새 폴더 (3)/IMG_9347.JPG", "30평대 아파트", "주방까지 따뜻하게 완성", "한샘 주방", 3.2),
    ("새 폴더 (2)/QMNX1119.JPG", "시공 전에는", "3D 설계로 방향을 먼저 잡고", "설계", 3.2),
    ("새 폴더 (2)/IMG_8467.JPG", "철거 후 보이는", "집의 진짜 상태를 확인합니다", "철거", 3.0),
    ("새 폴더 (2)/IMG_8662.JPG", "오래된 배관은", "마감 전에 꼼꼼히 정리하고", "설비", 3.1),
    ("새 폴더/IMG_9374.JPG", "욕실은", "바탕 공정부터 차근차근", "욕실 공정", 3.0),
    ("새 폴더 (3)/IMG_9330.JPG", "현관에는", "앉아서 신발 신는 벤치를", "현관", 3.3),
    ("새 폴더 (3)/IMG_9294.JPG", "거실은", "눈이 편한 조명과 밝은 톤으로", "거실", 3.5),
    ("새 폴더 (3)/IMG_9338.JPG", "식탁 공간은", "가족의 시간이 머무는 자리로", "다이닝", 3.3),
    ("새 폴더 (3)/IMG_9318.JPG", "욕실은", "차분하고 관리하기 쉽게", "욕실", 3.2),
    ("새 폴더 (3)/IMG_9314.JPG", "방은", "가구가 잘 어울리는 바탕으로", "방", 3.1),
    ("새 폴더 (3)/IMG_9346.JPG", "베란다까지", "밝고 쓰기 편하게 정리", "베란다", 3.0),
    ("새 폴더 (2)/XGYY9399.PNG", "가구가 들어오면", "집의 온기가 더 살아납니다", "입주 후", 3.4),
    ("새 폴더/HAFE7027.JPG", "구축 아파트 인테리어 전문", "세종인테리어와 함께하세요!", "SEJONG INTERIOR", 4.0),
]


def get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    names = ["malgunbd.ttf", "malgun.ttf"] if bold else ["malgun.ttf", "malgunbd.ttf"]
    for name in names:
        path = Path("C:/Windows/Fonts") / name
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


TAG_FONT = get_font(20, True)
TITLE_FONT = get_font(58, True)
SUB_FONT = get_font(38, False)


def ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) * (1 - t)


def load(src: str) -> Image.Image:
    return ImageOps.exif_transpose(Image.open(BLOG / src)).convert("RGB")


def cover(img: Image.Image, progress: float) -> Image.Image:
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
    zoom = 1.04 + 0.055 * ease(progress)
    resized = img.resize((int(w * zoom), int(h * zoom)), Image.Resampling.LANCZOS)
    x = (resized.width - WIDTH) // 2 + int(math.sin(progress * math.pi) * 18)
    y = (resized.height - HEIGHT) // 2 + int((progress - 0.5) * 34)
    x = max(0, min(x, resized.width - WIDTH))
    y = max(0, min(y, resized.height - HEIGHT))
    return resized.crop((x, y, x + WIDTH, y + HEIGHT))


def gradient() -> Image.Image:
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for y in range(HEIGHT):
        if y < HEIGHT * 0.35:
            a = int(120 * (1 - y / (HEIGHT * 0.35)))
        else:
            a = int(210 * ((y - HEIGHT * 0.35) / (HEIGHT * 0.65)) ** 1.55)
        draw.line((0, y, WIDTH, y), fill=(0, 0, 0, max(0, min(210, a))))
    return overlay


OVERLAY = gradient()


def wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, width: int) -> list[str]:
    words = text.split(" ")
    lines: list[str] = []
    line = ""
    for word in words:
        test = f"{line} {word}".strip()
        if draw.textlength(test, font=font) > width and line:
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
    appear = ease(min(1, p / 0.22))
    alpha = int(255 * appear)
    shift = int((1 - appear) * 34)
    left = 52
    bottom = 910 + shift

    draw.rounded_rectangle((left, 104 + shift, left + 228, 146 + shift), radius=21, fill=(205, 166, 102, int(alpha * 0.95)))
    draw.text((left + 20, 125 + shift), tag, font=TAG_FONT, fill=(18, 16, 12, alpha), anchor="lm")

    for line in wrap(draw, title, TITLE_FONT, WIDTH - left * 2)[:2]:
        draw.text((left + 2, bottom + 2), line, font=TITLE_FONT, fill=(0, 0, 0, int(alpha * 0.35)))
        draw.text((left, bottom), line, font=TITLE_FONT, fill=(255, 250, 240, alpha))
        bottom += 72

    bottom += 14
    for line in wrap(draw, sub, SUB_FONT, WIDTH - left * 2)[:2]:
        draw.text((left, bottom), line, font=SUB_FONT, fill=(255, 255, 255, int(alpha * 0.9)))
        bottom += 52

    draw.rounded_rectangle((52, HEIGHT - 70, WIDTH - 52, HEIGHT - 66), radius=2, fill=(255, 255, 255, 65))
    draw.rounded_rectangle((52, HEIGHT - 70, 52 + int((WIDTH - 104) * total_p), HEIGHT - 66), radius=2, fill=(205, 166, 102, 230))
    return frame.convert("RGB")


def main() -> None:
    if not FFMPEG.exists():
        raise FileNotFoundError(f"ffmpeg not found: {FFMPEG}")

    assets = [load(scene[0]) for scene in SCENES]
    total = sum(scene[4] for scene in SCENES)
    POSTER.parent.mkdir(parents=True, exist_ok=True)
    draw_frame(assets[0], SCENES[0], 0, 0).save(POSTER, quality=92)

    cmd = [
        str(FFMPEG),
        "-y",
        "-f",
        "rawvideo",
        "-vcodec",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s",
        f"{WIDTH}x{HEIGHT}",
        "-r",
        str(FPS),
        "-i",
        "-",
        "-an",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        "-crf",
        "21",
        str(OUTPUT),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    elapsed = 0.0
    assert proc.stdin is not None
    for i, scene in enumerate(SCENES):
        frames = max(1, round(scene[4] * FPS))
        for n in range(frames):
            p = n / max(1, frames - 1)
            frame = draw_frame(assets[i], scene, p, elapsed / total)
            proc.stdin.write(frame.tobytes())
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
