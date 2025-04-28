from PIL import Image
import numpy as np
from rembg import remove  # 用于更精确的背景移除
import os

# 定义身份证号（需要用户提供，这里只是示例）
student_id = "1111111111111111111"  # 替换为实际身份证号

# 输入照片路径（用户提供的照片路径）
input_image_path = "/home/qianeric/下载/1.jpeg"  # 替换为实际照片路径

# 输出照片路径（以身份证号命名）
output_image_path = f"{student_id}.jpg"

# 目标像素尺寸（295x413 像素，符合小一寸照片比例）
target_width_px = 295
target_height_px = 413

# 目标物理尺寸（2.7cm x 3.8cm，转换为像素需要 DPI）
DPI = 300  # 使用 300 DPI（每英寸像素数）
target_width_cm = 2.7  # 宽 2.7cm
target_height_cm = 3.8  # 高 3.8cm

# 计算目标尺寸（厘米转像素）
target_width_px = int(target_width_cm * DPI / 2.54)  # 1 英寸 = 2.54 厘米
target_height_px = int(target_height_cm * DPI / 2.54)

# 目标文件大小（5MB 以内）
max_file_size = 5 * 1024 * 1024  # 5MB 转换为字节

# 红色底色 (RGB)
background_color = (255, 0, 0)  # 红色

try:
    # 打开原始照片
    image = Image.open(input_image_path).convert("RGBA")

    # 使用 rembg 移除背景
    image_no_bg = remove(image)

    # 调整照片大小到目标像素尺寸
    image_no_bg = image_no_bg.resize((target_width_px, target_height_px), Image.LANCZOS)

    # 创建红色背景
    background = Image.new("RGBA", (target_width_px, target_height_px), background_color + (255,))

    # 将人物图像粘贴到红色背景上
    final_image = Image.alpha_composite(background, image_no_bg)

    # 转换为 RGB 模式并保存为 jpg
    final_image = final_image.convert("RGB")
    final_image.save(output_image_path, "JPEG", quality=95)

    # 检查文件大小并调整质量以满足 5MB 限制
    file_size = os.path.getsize(output_image_path)
    quality = 95
    while file_size > max_file_size and quality > 10:
        quality -= 5
        final_image.save(output_image_path, "JPEG", quality=quality)
        file_size = os.path.getsize(output_image_path)

    # 确认最终文件信息
    print(f"照片已保存为: {output_image_path}")
    print(f"最终文件大小: {file_size / (1024 * 1024):.2f} MB")
    print(f"照片像素: {target_width_px}x{target_height_px}")
    print(f"照片底色: 红色")

except Exception as e:
    print(f"处理照片时出错: {e}")
