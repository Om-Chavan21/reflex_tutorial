import os
from PIL import Image
import shutil
from pathlib import Path

IMAGE_EXTENSIONS = [
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".webp",
    ".tiff",
    ".tif",
    ".ico",
    ".jfif",
    ".pjpeg",
    ".pjp",
    ".avif",
    ".heic",
    ".heif",
]


def convert_images_to_jpg(input_folder: str):
    """
    Converts all supported image files in input folder to JPG format.
    Creates a JPG_CONVERTED folder and moves converted images there.
    Deletes original files after conversion.
    """
    # Convert input to Path object
    input_path = Path(input_folder)

    # Create JPG_CONVERTED folder if it doesn't exist
    output_folder = input_path / "JPG_CONVERTED"
    output_folder.mkdir(exist_ok=True)

    # Find all image files recursively
    for file_path in input_path.rglob("*"):
        if file_path.suffix.lower() in IMAGE_EXTENSIONS:
            try:
                # Skip if file is already in JPG_CONVERTED
                if "JPG_CONVERTED" in str(file_path):
                    continue

                # Open and convert image
                with Image.open(file_path) as img:
                    # Convert to RGB if necessary (for PNG with transparency etc)
                    if img.mode in ("RGBA", "LA", "P"):
                        img = img.convert("RGB")

                    # Create output filename
                    output_path = output_folder / f"{file_path.stem}.jpg"

                    # Save as JPG
                    img.save(output_path, "JPEG", quality=95)

                    # Delete original file after successful conversion
                    file_path.unlink()

                print(f"Converted: {file_path.name} -> {output_path.name}")

            except Exception as e:
                print(f"Error converting {file_path.name}: {str(e)}")


if __name__ == "__main__":
    # Example usage
    folder_path = "/path/to/your/input/folder"
    convert_images_to_jpg(folder_path)
