from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEPS = ROOT / "_video_deps"
if DEPS.exists():
    sys.path.insert(0, str(DEPS))

import imageio.v2 as imageio
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps


WIDTH = 720
HEIGHT = 1280
FPS = 24
SCALE = WIDTH / 1080
OUTPUT = ROOT / "bupyeong-donga-2danji-sejong-shorts.mp4"
POSTER = ROOT / "bupyeong-donga-2danji-sejong-shorts-poster.jpg"


SCENES = [
    {
        "title": "30평 구축 아파트의 변화",
        "sub": "부평 동아아파트 2단지",
        "tag": "SEJONG INTERIOR",
        "src": "새 폴더 (3)/IMG_9294.JPG",
        "duration": 3.2,
    },
    {
        "title": "완성된 주방의 첫인상",
        "sub": "한샘 주방과 따뜻한 다이닝",
        "tag": "KITCHEN",
        "src": "새 폴더 (3)/IMG_9347.JPG",
        "duration": 3.1,
    },
    {
        "title": "도면과 3D로 먼저 맞춘 방향",
        "sub": "현관 벤치, 주방 동선, 수납 계획",
        "tag": "PLANNING",
        "src": "새 폴더 (2)/QMNX1119.JPG",
        "duration": 3.4,
        "contain": True,
    },
    {
        "title": "오래된 집은 철거가 시작입니다",
        "sub": "벽, 바닥, 배관 위치를 먼저 확인",
        "tag": "BEFORE",
        "src": "새 폴더 (2)/IMG_8467.JPG",
        "duration": 3.2,
    },
    {
        "title": "보이지 않는 배관까지 정리",
        "sub": "수도관과 가지관 교체 범위 확인",
        "tag": "PLUMBING",
        "src": "새 폴더 (2)/IMG_8661.JPG",
        "duration": 3.3,
    },
    {
        "title": "욕실 바탕 공정도 꼼꼼하게",
        "sub": "방수와 타일 마감 전 단계",
        "tag": "BATH PROCESS",
        "src": "새 폴더/IMG_9374.JPG",
        "duration": 3.2,
    },
    {
        "title": "눈이 편안한 거실 조명",
        "sub": "천장 평탄화와 엣지등으로 단정하게",
        "tag": "LIVING",
        "src": "새 폴더 (3)/IMG_9322.JPG",
        "duration": 4.0,
    },
    {
        "title": "현관에는 앉을 수 있는 벤치",
        "sub": "매일의 동작을 편하게 만든 첫 공간",
        "tag": "ENTRANCE",
        "src": "새 폴더 (3)/IMG_9330.JPG",
        "duration": 3.4,
    },
    {
        "title": "화이트와 우드가 만난 한샘 주방",
        "sub": "밝지만 차갑지 않은 조리 공간",
        "tag": "HANSSEM",
        "src": "새 폴더 (3)/IMG_9348.JPG",
        "duration": 4.0,
    },
    {
        "title": "차분한 톤의 욕실 완성",
        "sub": "관리하기 쉽고 오래 질리지 않는 마감",
        "tag": "BATHROOM",
        "src": "새 폴더 (3)/IMG_9318.JPG",
        "duration": 3.6,
    },
    {
        "title": "방은 가구가 들어오기 좋은 바탕으로",
        "sub": "밝은 벽과 바닥, 편안한 조도",
        "tag": "ROOM",
        "src": "새 폴더 (3)/IMG_9314.JPG",
        "duration": 3.6,
    },
    {
        "title": "베란다와 세탁실까지 밝게",
        "sub": "쓰기 편한 마감과 물 사용 동선",
        "tag": "BALCONY",
        "src": "새 폴더 (3)/IMG_9346.JPG",
        "duration": 3.3,
    },
    {
        "title": "가구가 들어오며 더 따뜻해진 집",
        "sub": "은퇴 부부의 일상이 편안하게 머무는 공간",
        "tag": "AFTER LIVING",
        "src": "새 폴더 (2)/XGYY9399.PNG",
        "duration": 4.1,
    },
    {
        "title": "부평 동아아파트 2단지",
        "sub": "세종인테리어 시공 사례",
        "tag": "SEJONG INTERIOR",
        "src": "새 폴더/HAFE7027.JPG",
        "duration": 3.2,
    },
]


def font(size: int, weight: str = "regular") -> ImageFont.FreeTypeFont:
    candidates = [
        Path("C:/Windows/Fonts/malgunbd.ttf") if weight == "bold" else Path("C:/Windows/Fonts/malgun.ttf"),
        Path("C:/Windows/Fonts/NotoSansKR-Bold.ttf") if weight == "bold" else Path("C:/Windows/Fonts/NotoSansKR-Regular.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


FONT_TAG = font(round(30 * SCALE), "bold")
FONT_TITLE = font(round(78 * SCALE), "bold")
FONT_SUB = font(round(40 * SCALE))


def ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    if t < 0.5:
        return 2 * t * t
    return 1 - ((-2 * t + 2) ** 2) / 2


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font_obj: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    words = text.split(" ")
    lines: list[str] = []
    line = ""
    for word in words:
        test = f"{line} {word}".strip()
        if draw.textlength(test, font=font_obj) > max_width and line:
            lines.append(line)
            line = word
        else:
            line = test
    if line:
        lines.append(line)
    return lines


def load_image(src: str) -> Image.Image:
    path = ROOT / src
    image = Image.open(path)
    image = ImageOps.exif_transpose(image).convert("RGB")
    return image


def cover_image(image: Image.Image, progress: float, contain: bool = False) -> Image.Image:
    image = ImageEnhance.Color(image).enhance(1.03)
    image = ImageEnhance.Contrast(image).enhance(1.04)

    if contain:
        bg = image.copy()
        bg.thumbnail((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
        blur = ImageOps.fit(image, (WIDTH, HEIGHT), method=Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(34))
        blur = ImageEnhance.Brightness(blur).enhance(0.42)
        scale = min((WIDTH * 0.92) / image.width, (HEIGHT * 0.78) / image.height)
        fitted = image.resize((int(image.width * scale), int(image.height * scale)), Image.Resampling.LANCZOS)
        x = (WIDTH - fitted.width) // 2
        y = int(HEIGHT * 0.22)
        blur.paste(fitted, (x, y))
        return blur

    image_ratio = image.width / image.height
    canvas_ratio = WIDTH / HEIGHT
    if image_ratio > canvas_ratio:
        base_h = HEIGHT
        base_w = int(HEIGHT * image_ratio)
    else:
        base_w = WIDTH
        base_h = int(WIDTH / image_ratio)

    zoom = 1.045 + progress * 0.055
    resized = image.resize((int(base_w * zoom), int(base_h * zoom)), Image.Resampling.LANCZOS)
    pan_x = int(math.sin(progress * math.pi) * 28)
    pan_y = int((progress - 0.5) * 48)
    left = (resized.width - WIDTH) // 2 - pan_x
    top = (resized.height - HEIGHT) // 2 - pan_y
    left = max(0, min(left, max(0, resized.width - WIDTH)))
    top = max(0, min(top, max(0, resized.height - HEIGHT)))
    return resized.crop((left, top, left + WIDTH, top + HEIGHT))


def make_gradient_overlay() -> Image.Image:
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    arr = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8)
    for y in range(HEIGHT):
        if y < HEIGHT * 0.42:
            alpha = int(150 * (1 - y / (HEIGHT * 0.42)))
        elif y > HEIGHT * 0.42:
            alpha = int(190 * ((y - HEIGHT * 0.42) / (HEIGHT * 0.58)) ** 1.45)
        else:
            alpha = 0
        arr[y, :, 3] = max(0, min(190, alpha))
    return Image.fromarray(arr, "RGBA")


GRADIENT_OVERLAY = make_gradient_overlay()


def add_gradient(frame: Image.Image) -> Image.Image:
    return Image.alpha_composite(frame.convert("RGBA"), GRADIENT_OVERLAY).convert("RGB")


def draw_text(frame: Image.Image, scene: dict[str, object], local_progress: float, total_progress: float) -> Image.Image:
    frame = frame.convert("RGBA")
    draw = ImageDraw.Draw(frame)
    appear = ease(min(1.0, local_progress / 0.22))
    y_shift = int((1 - appear) * 40 * SCALE)
    alpha = int(255 * appear)

    left = round(78 * SCALE)
    max_width = WIDTH - left * 2
    tag_w = round(320 * SCALE)
    tag_h = round(62 * SCALE)
    tag_box = Image.new("RGBA", (tag_w, tag_h), (0, 0, 0, 0))
    tag_draw = ImageDraw.Draw(tag_box)
    tag_draw.rounded_rectangle((0, 0, tag_w, tag_h), radius=round(31 * SCALE), fill=(201, 164, 106, int(alpha * 0.94)))
    tag_draw.text((round(28 * SCALE), tag_h // 2), str(scene["tag"]), font=FONT_TAG, fill=(20, 18, 13, alpha), anchor="lm")
    frame.alpha_composite(tag_box, (left, round(130 * SCALE) + y_shift))

    title_lines = wrap_text(draw, str(scene["title"]), FONT_TITLE, max_width)[:3]
    title_y = round((1380 - len(title_lines) * 44) * SCALE) + y_shift
    for line in title_lines:
        draw.text((left + round(3 * SCALE), title_y + round(3 * SCALE)), line, font=FONT_TITLE, fill=(0, 0, 0, int(alpha * 0.28)))
        draw.text((left, title_y), line, font=FONT_TITLE, fill=(255, 250, 240, alpha))
        title_y += round(92 * SCALE)

    sub_lines = wrap_text(draw, str(scene["sub"]), FONT_SUB, max_width)[:2]
    title_y += round(22 * SCALE)
    for line in sub_lines:
        draw.text((left, title_y), line, font=FONT_SUB, fill=(255, 255, 255, int(alpha * 0.86)))
        title_y += round(56 * SCALE)

    bar_left = round(78 * SCALE)
    bar_top = HEIGHT - round(96 * SCALE)
    bar_h = max(4, round(5 * SCALE))
    bar_width = int((WIDTH - bar_left * 2) * total_progress)
    draw.rounded_rectangle((bar_left, bar_top, WIDTH - bar_left, bar_top + bar_h), radius=3, fill=(255, 255, 255, 70))
    draw.rounded_rectangle((bar_left, bar_top, bar_left + bar_width, bar_top + bar_h), radius=3, fill=(201, 164, 106, 220))
    return frame.convert("RGB")


def render_frame(scene_index: int, local_progress: float, elapsed: float, assets: list[Image.Image], total_duration: float) -> Image.Image:
    scene = SCENES[scene_index]
    image = assets[scene_index]
    frame = cover_image(image, ease(local_progress), bool(scene.get("contain")))
    frame = add_gradient(frame)
    return draw_text(frame, scene, local_progress, elapsed / total_duration)


def main() -> None:
    total_duration = sum(float(scene["duration"]) for scene in SCENES)
    assets = [load_image(str(scene["src"])) for scene in SCENES]

    poster_frame = render_frame(0, 0, 0, assets, total_duration)
    poster_frame.save(POSTER, quality=92)

    writer = imageio.get_writer(
        OUTPUT,
        fps=FPS,
        codec="libx264",
        quality=8,
        macro_block_size=1,
        ffmpeg_params=["-pix_fmt", "yuv420p", "-movflags", "+faststart"],
    )

    elapsed = 0.0
    try:
        for scene_index, scene in enumerate(SCENES):
            duration = float(scene["duration"])
            frame_count = max(1, round(duration * FPS))
            for frame_number in range(frame_count):
                local_progress = frame_number / max(1, frame_count - 1)
                frame = render_frame(scene_index, local_progress, elapsed, assets, total_duration)
                writer.append_data(np.asarray(frame))
                elapsed += 1 / FPS
    finally:
        writer.close()

    print(f"created={OUTPUT}")
    print(f"poster={POSTER}")
    print(f"duration={total_duration:.1f}s fps={FPS} size={WIDTH}x{HEIGHT}")


if __name__ == "__main__":
    main()
