from PIL import Image
import os

def images_to_pdf(image_folder, output_pdf):
    # 获取文件夹中所有 JPG 文件
    image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.lower().endswith('.jpg')]
    # 按文件名排序
    image_files.sort()

    images = []
    for img_path in image_files:
        img = Image.open(img_path).convert('RGB')
        images.append(img)

    if images:
        first_image = images[0]
        # 保存为 PDF 文件
        first_image.save(output_pdf, save_all=True, append_images=images[1:])
