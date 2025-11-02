# Future updates: "even smaller" optional argument that resizes the image even smaller than current --small argument
#                 "usage" and help argument that shows how to use script

import argparse
import os
from PIL import Image, ImageDraw

def process_image(input_path, output_path, size_mode="small", sizing=None):
    """
    Process an image by flipping it upside down, optionally resizing, and adding crosshairs.
    
    Args:
        input_path (str): Path to input image
        output_path (str): Path to save output image
        size_mode (str): "original" to keep original size, "small" for 576x720, "smallest" for 300x420
    """
    # Open the image
    img = Image.open(input_path)
    original_width, original_height = img.size
    
    # Flip image upside down and mirror horizontally
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    img = img.transpose(Image.FLIP_LEFT_RIGHT)
    
    # Determine final dimensions
    if sizing is not None:
        width_px, height_px = sizing
        img = img.resize((width_px, height_px), Image.Resampling.LANCZOS)
    elif size_mode == "original":
        width_px, height_px = original_width, original_height
    elif size_mode == "smallest":
        width_px, height_px = 300, 420
        img = img.resize((width_px, height_px), Image.Resampling.LANCZOS)
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
                       help="Output image path (default: derived from input: name_DRSB.ext)")
    parser.add_argument("--original", action="store_true", 
                       help="Keep original image size (default: resize to 576x720)")
    parser.add_argument("--small", action="store_true", 
                       help="Resize to 576x720 pixels (default behavior)")
    parser.add_argument("--smallest", action="store_true",
                        help="Resizes images to 300x420 (default: resize to 576x720)")
    parser.add_argument("--sizing", type=str, default=None,
                        help="Custom size as WxH (e.g., 800x600) or W,H")
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.exists(args.input_image):
        print(f"Error: Input file '{args.input_image}' not found")
        return 1

    # Determine output path: if user didn't override default, derive from input name
    output_path = args.output
    if output_path == "output.png":
        in_dir = os.path.dirname(args.input_image)
        in_base = os.path.basename(args.input_image)
        stem, ext = os.path.splitext(in_base)
        # If input has no extension, default to .png
        if not ext:
            ext = ".png"
        output_path = os.path.join(in_dir, f"{stem}_DRSB{ext}")

    # Parse custom sizing if provided
    custom_size = None
    if args.sizing:
        s = args.sizing.lower().replace(" ", "")
        if "x" in s:
            parts = s.split("x")
        else:
            parts = s.split(",")
        if len(parts) == 2:
            try:
                w = int(parts[0])
                h = int(parts[1])
                if w > 0 and h > 0:
                    custom_size = (w, h)
                else:
                    print("Error: --sizing values must be positive integers")
                    return 1
            except ValueError:
                print("Error: --sizing must be in the form WxH or W,H with integers, e.g., 800x600")
                return 1
        else:
            print("Error: --sizing must be in the form WxH or W,H with integers, e.g., 800x600")
            return 1
    # Determine size mode
    if custom_size is not None:
        size_mode = "custom"
    elif args.original:
        size_mode = "original"
    elif args.smallest:
        size_mode = "smallest"
    else:
        size_mode = "small"  # default behavior
    
    # Process the image
    try:
        process_image(args.input_image, output_path, size_mode, sizing=custom_size)
        return 0
    except Exception as e:
        print(f"Error processing image: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
