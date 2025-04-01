import os

from PIL import Image

# 원본 이미지 경로
source_image = "icon.png"

# iconset 폴더 생성
iconset_dir = "MyIcon.iconset"
os.makedirs(iconset_dir, exist_ok=True)

# 아이콘 사이즈 리스트
sizes = [
    (16, "icon_16x16.png"),
    (32, "icon_16x16@2x.png"),
    (32, "icon_32x32.png"),
    (64, "icon_32x32@2x.png"),
    (128, "icon_128x128.png"),
    (256, "icon_128x128@2x.png"),
    (256, "icon_256x256.png"),
    (512, "icon_256x256@2x.png"),
    (512, "icon_512x512.png"),
    (1024, "icon_512x512@2x.png"),
]

# 이미지 리사이즈 후 저장
img = Image.open(source_image)
for size, filename in sizes:
    resized_image = img.resize((size, size), Image.LANCZOS)
    resized_image.save(os.path.join(iconset_dir, filename))

print("아이콘 세트 생성 완료: MyIcon.iconset")
