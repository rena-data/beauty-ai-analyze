"""이미지 전처리 유틸리티"""

from PIL import Image

MAX_SIZE = 512
MAX_FILE_MB = 10
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/heic"}


def validate_image(uploaded_file) -> tuple[bool, str]:
    """업로드된 파일 검증. (통과 여부, 메시지) 반환."""
    if uploaded_file is None:
        return False, "파일이 선택되지 않았습니다."

    if uploaded_file.type not in ALLOWED_TYPES:
        return False, f"지원하지 않는 파일 형식입니다: {uploaded_file.type}"

    size_mb = uploaded_file.size / (1024 * 1024)
    if size_mb > MAX_FILE_MB:
        return False, f"파일 크기가 너무 큽니다: {size_mb:.1f}MB (최대 {MAX_FILE_MB}MB)"

    return True, "검증 완료"


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
