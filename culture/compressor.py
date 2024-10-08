from PIL import Image
import base64
import io

def process_and_save_image(input_image_path, output_image_path, base64_output_path, target_size_kb=1):
    # Open image and convert to grayscale (L mode)
    img = Image.open(input_image_path).convert("L")  # Convert to grayscale (black and white)

    # Binarize the image (convert to black and white only)
    threshold = 128
    img = img.point(lambda p: p > threshold and 255)  # Set threshold to convert to pure black and white

    # Convert the white pixels to transparency and black to black (RGBA mode)
    img = img.convert("RGBA")
    datas = img.getdata()
    new_data = []

    for item in datas:
        # If it's white, make it transparent; if it's black, keep it
        if item[0] == 255:
            new_data.append((255, 255, 255, 0))  # Make white transparent
        else:
            new_data.append((0, 0, 0, 255))  # Keep black opaque

    img.putdata(new_data)

    # Quantize the image to 2 colors (black and transparent) to minimize file size
    img = img.quantize(colors=2, method=Image.FASTOCTREE)

    # Initialize resizing dimensions
    width, height = img.size

    # Loop to continue compressing until we reach the target size
    compressed_image = io.BytesIO()
    while True:
        # Resize the image if needed to reduce the size
        if width > 100 and height > 100:
            img = img.resize((width, height), Image.LANCZOS)

        # Save the image in PNG format and check size
        compressed_image.seek(0)
        img.save(compressed_image, format='PNG', optimize=True)

        size_kb = len(compressed_image.getvalue()) / 1024  # Convert bytes to KB
        if size_kb <= target_size_kb:
            break

        # Shrink the dimensions by 10% if still too large
        width = int(width * 0.9)
        height = int(height * 0.9)

        # If it reaches too small, throw a warning (but it won't fail)
        if width < 5 or height < 5:
            print("Warning: Image has been downsized significantly to meet the target size.")
            break

    # Save the final compressed image
    with open(output_image_path, 'wb') as f:
        f.write(compressed_image.getvalue())

    # Encode the image to base64
    compressed_image.seek(0)
    img_base64 = base64.b64encode(compressed_image.getvalue()).decode('utf-8')

    # Save the base64 to a text file
    with open(base64_output_path, 'w') as f:
        f.write(img_base64)

    return img_base64


# Example usage:
input_image_path = "images/elon.png"  # Replace with your input file path (WEBP, JPEG, etc.)
output_image_path = "compressed/output_image.png"  # Path where the output image will be saved
base64_output_path = "base64/output_base64.txt"  # Path to save the base64 string

target_size_kb = 1  # Set your target size, in this case, 1KB

base64_img = process_and_save_image(input_image_path, output_image_path, base64_output_path, target_size_kb)
print("Base64 Output saved to text file.")