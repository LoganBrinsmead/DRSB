import argparse
import os
from PIL import Image, ImageDraw

def process_image(input_path, output_path, size_mode="small"):
    """
    Process an image by flipping it upside down, optionally resizing, and adding crosshairs.
    
    Args:
        input_path (str): Path to input image
        output_path (str): Path to save output image
        size_mode (str): "original" to keep original size, "small" for 576x720
    """
    # Open the image
    img = Image.open(input_path)
    original_width, original_height = img.size
    
    # Flip image upside down and mirror horizontally
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    img = img.transpose(Image.FLIP_LEFT_RIGHT)
    
    # Determine final dimensions
    if size_mode == "original":
        width_px, height_px = original_width, original_height
    else:  # small mode
        width_px, height_px = 576, 720
        # Resize with high-quality resampling
        img = img.resize((width_px, height_px), Image.Resampling.LANCZOS)

    # Draw crosshairs
    draw = ImageDraw.Draw(img)
    center_x = width_px // 2
    center_y = height_px // 2

    # Draw black lines across the center
    draw.line([(0, center_y), (width_px, center_y)], fill='black', width=1)
    draw.line([(center_x, 0), (center_x, height_px)], fill='black', width=1)

    # Save with high quality
    img.save(output_path, quality=95, optimize=True)
    print(f"[+] Saved: {output_path} ({width_px}x{height_px}px)")

def main():
    parser = argparse.ArgumentParser(
        description="Process images: flip upside down, optionally resize, and add crosshairs"
    )
    parser.add_argument("input_image", help="Path to input image file")
    parser.add_argument("-o", "--output", default="output.png", 
                       help="Output image path (default: output.png)")
    parser.add_argument("--original", action="store_true", 
                       help="Keep original image size (default: resize to 576x720)")
    parser.add_argument("--small", action="store_true", 
                       help="Resize to 576x720 pixels (default behavior)")
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.exists(args.input_image):
        print(f"Error: Input file '{args.input_image}' not found")
        return 1
    
    # Determine size mode
    if args.original:
        size_mode = "original"
    else:
        size_mode = "small"  # default behavior
    
    # Process the image
    try:
        process_image(args.input_image, args.output, size_mode)
        return 0
    except Exception as e:
        print(f"Error processing image: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
