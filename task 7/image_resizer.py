import os
from PIL import Image

input_folder = "images"        
output_folder = "resized_images"  

os.makedirs(output_folder, exist_ok=True)

size = (150, 100)

for filename in os.listdir(input_folder):
    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path)
                
        img_resized = img.resize(size)
        output_path = os.path.join(output_folder, filename)
        img_resized.save(output_path)

        print(f"Resized and saved: {output_path}")

print(" All images resized and saved successfully!")
