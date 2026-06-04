"""이미지 전처리 유틸리티"""

from PIL import Image

MAX_SIZE = 512


def resize_for_analysis(image: Image.Image) -> Image.Image:
    """분석용으로 이미지 리사이즈 (512px, 토큰 절감)"""
    if image.mode != "RGB":
        image = image.convert("RGB")

    w, h = image.size
    if max(w, h) <= MAX_SIZE:
        return image

    if w > h:
        new_w = MAX_SIZE
        new_h = int(h * MAX_SIZE / w)
    else:
        new_h = MAX_SIZE
        new_w = int(w * MAX_SIZE / h)

    return image.resize((new_w, new_h), Image.LANCZOS)
