from PIL import Image
import base64
import io

def process_and_save_image(input_image_path, output_image_path, base64_output_path, svg_output_path, target_size_kb=1):
    # Open image and convert to grayscale (L mode)
    img = Image.open(input_image_path).convert("L")  # Convert to grayscale (black and white)

    # Adaptive thresholding (Otsu method) to binarize more effectively
    threshold = 128
    img = img.point(lambda p: p > threshold and 255)  # Binary threshold to black/white

    # Convert to black and transparent (RGBA mode) to do artsy manipulations
    img = img.convert("RGBA")
    datas = img.getdata()
    new_data = []
    for item in datas:
        if item[0] > 128:
            new_data.append((255, 255, 255, 0))  # White to transparent
        else:
            new_data.append((0, 0, 0, 255))  # Black remains opaque

    img.putdata(new_data)

    # Quantize the image using FASTOCTREE method (valid for RGBA)
    img = img.quantize(colors=2, method=Image.FASTOCTREE)

    # After artsy manipulation, convert image to 'P' mode for indexed color
    img = img.convert("P", palette=Image.ADAPTIVE)

    # Optimize the PNG compression level
    compressed_image = io.BytesIO()
    img.save(compressed_image, format='PNG', optimize=True)

    # Check size and resize if needed
    size_kb = len(compressed_image.getvalue()) / 1024  # Size in KB
    if size_kb > target_size_kb:
        # Resize the image progressively only if needed
        width, height = img.size
        while size_kb > target_size_kb and width > 300 and height > 300:
            width = int(width * 0.9)
            height = int(height * 0.9)
            img = img.resize((width, height), Image.LANCZOS)
            compressed_image.seek(0)
            img.save(compressed_image, format='PNG', optimize=True)
            size_kb = len(compressed_image.getvalue()) / 1024

    # Save the final image
    with open(output_image_path, 'wb') as f:
        f.write(compressed_image.getvalue())

    # Strip image metadata to further reduce size
    compressed_image.seek(0)
    img_no_metadata = Image.open(compressed_image)
    compressed_image.seek(0)
    stripped_image = io.BytesIO()
    img_no_metadata.save(stripped_image, format='PNG', optimize=True)

    # Base64 encode the stripped image
    stripped_image.seek(0)
    img_base64 = base64.b64encode(stripped_image.getvalue()).decode('utf-8')

    # Save the base64 string
    with open(base64_output_path, 'w') as f:
        f.write(img_base64)

    # Calculate and print the final file size in KB
    final_size_kb = len(stripped_image.getvalue()) / 1024
    print(f"Final image file size: {final_size_kb:.2f} KB")

    # Create an SVG file that embeds the base64 image and adds CSS for flashing RGB colors
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200">
    <style>
        @keyframes flash {{
            0% {{ filter: hue-rotate(0deg); }}
            33% {{ filter: hue-rotate(120deg); }}
            66% {{ filter: hue-rotate(240deg); }}
            100% {{ filter: hue-rotate(360deg); }}
        }}
        image {{
            animation: flash 3s infinite;
        }}
    </style>
    <image href="data:image/png;base64,{img_base64}" width="200" height="200" />
</svg>'''

    # Save the SVG to the file
    with open(svg_output_path, 'w') as f:
        f.write(svg_content)

    print(f"SVG with flashing RGB effect saved to {svg_output_path}")

    return img_base64


# Example usage:
input_image_path = "images/rat.png"  # Input file
output_image_path = "compressed/output_image.png"  # Compressed output file path
base64_output_path = "base64/output_base64.txt"  # Base64 output file path
svg_output_path = "svg/output_image.svg"  # SVG output file path

target_size_kb = 1  # Target size in KB

base64_img = process_and_save_image(input_image_path, output_image_path, base64_output_path, svg_output_path, target_size_kb)
print("Base64 Output saved to text file and SVG with RGB flash saved.")