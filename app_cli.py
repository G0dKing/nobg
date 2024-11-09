import sys
from PIL import Image
import rembg
import io

def remove_background(image_path):
    with open(image_path, "rb") as input_file:
        input_data = input_file.read()
    output_data = rembg.remove(input_data)
    return Image.open(io.BytesIO(output_data))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python no_bg.py <input_image> <output_image>")
        sys.exit(1)

    input_image = sys.argv[1]
    output_image = sys.argv[2]
    
    processed_image = remove_background(input_image)
    processed_image.save(output_image)
    print(f"Background removed image saved as {output_image}")
