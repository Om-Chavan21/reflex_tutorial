import subprocess
import concurrent.futures
from pathlib import Path
from tqdm import tqdm

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


def convert_single_image(file_path: Path, output_folder: Path) -> tuple[bool, str]:
    """Convert a single image to JPG using ffmpeg"""
    try:
        output_path = output_folder / f"{file_path.stem}.jpg"
        cmd = [
            "ffmpeg",
            "-i",
            str(file_path),
            "-quality",
            "95",
            "-y",  # Overwrite output files
            str(output_path),
        ]

        subprocess.run(cmd, capture_output=True, check=True)
        file_path.unlink()  # Delete original after successful conversion
        return True, file_path.name
    except subprocess.CalledProcessError as e:
        return False, f"Error converting {file_path.name}: {e.stderr.decode()}"


def convert_images_to_jpg(input_folder: str, max_workers: int = 4):
    """
    Converts all supported image files to JPG format using ffmpeg.
    Uses parallel processing for better performance.
    """
    input_path = Path(input_folder)
    output_folder = input_path / "JPG_CONVERTED"
    output_folder.mkdir(exist_ok=True)

    # Find all eligible image files
    image_files = [
        f
        for f in input_path.rglob("*")
        if f.suffix.lower() in IMAGE_EXTENSIONS and "JPG_CONVERTED" not in str(f)
    ]

    if not image_files:
        print("No images found to convert")
        return

    # Convert images in parallel with progress bar
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(convert_single_image, f, output_folder) for f in image_files
        ]

        with tqdm(total=len(image_files), desc="Converting images") as pbar:
            for future in concurrent.futures.as_completed(futures):
                success, msg = future.result()
                if success:
                    pbar.write(f"Converted: {msg}")
                else:
                    pbar.write(msg)
                pbar.update(1)


if __name__ == "__main__":
    folder_path = (
        "/Users/omchavan/Documents/projects/reflex_tutorial/insta_pro-jan-2025"
    )
    convert_images_to_jpg(folder_path)
