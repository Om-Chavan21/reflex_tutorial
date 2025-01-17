import subprocess
import concurrent.futures
from pathlib import Path
from tqdm import tqdm
import shutil

# File extensions
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

VIDEO_EXTENSIONS = [
    ".mp4",
    ".avi",
    ".mov",
    ".mkv",
    ".wmv",
    ".flv",
    ".webm",
    ".m4v",
    ".3gp",
    ".mpg",
    ".mpeg",
    ".m2v",
    ".ogv",
    ".mts",
    ".ts",
    ".vob",
]


def convert_single_image(file_path: Path, output_folder: Path) -> tuple[bool, str]:
    """Convert a single image to JPG using ffmpeg"""
    try:
        output_path = output_folder / f"{file_path.stem}.jpg"

        # If already JPG, just move
        if file_path.suffix.lower() in [".jpg", ".jpeg"]:
            shutil.move(file_path, output_path)
            return True, f"Copied JPG: {file_path.name}"

        cmd = ["ffmpeg", "-i", str(file_path), "-quality", "95", "-y", str(output_path)]
        subprocess.run(cmd, capture_output=True, check=True)
        file_path.unlink()
        return True, file_path.name
    except Exception as e:
        return False, f"Error processing {file_path.name}: {str(e)}"


def convert_single_video(file_path: Path, output_folder: Path) -> tuple[bool, str]:
    """Convert a single video to MP4 using ffmpeg"""
    try:
        output_path = output_folder / f"{file_path.stem}.mp4"

        # If already MP4, just move
        if file_path.suffix.lower() == ".mp4":
            shutil.move(file_path, output_path)
            return True, f"Copied MP4: {file_path.name}"

        cmd = [
            "ffmpeg",
            "-i",
            str(file_path),
            "-c:v",
            "libx264",
            "-crf",
            "23",
            "-preset",
            "medium",
            "-c:a",
            "aac",
            "-y",
            str(output_path),
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        file_path.unlink()
        return True, file_path.name
    except Exception as e:
        return False, f"Error processing {file_path.name}: {str(e)}"


def convert_media(input_folder: str, media_type: str = "both", max_workers: int = 4):
    """Convert images and/or videos in parallel"""
    input_path = Path(input_folder)

    # Setup output folders
    img_output = input_path / "JPG_CONVERTED"
    vid_output = input_path / "MP4_CONVERTED"

    if media_type in ["both", "images"]:
        img_output.mkdir(exist_ok=True)
    if media_type in ["both", "videos"]:
        vid_output.mkdir(exist_ok=True)

    # Find media files
    files = []
    if media_type in ["both", "images"]:
        files.extend(
            [
                (f, "image")
                for f in input_path.rglob("*")
                if f.suffix.lower() in IMAGE_EXTENSIONS and "CONVERTED" not in str(f)
            ]
        )
    if media_type in ["both", "videos"]:
        files.extend(
            [
                (f, "video")
                for f in input_path.rglob("*")
                if f.suffix.lower() in VIDEO_EXTENSIONS and "CONVERTED" not in str(f)
            ]
        )

    if not files:
        print("No media files found to convert")
        return

    # Convert files in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for f, type_ in files:
            if type_ == "image":
                futures.append(executor.submit(convert_single_image, f, img_output))
            else:
                futures.append(executor.submit(convert_single_video, f, vid_output))

        with tqdm(total=len(files), desc="Converting media") as pbar:
            for future in concurrent.futures.as_completed(futures):
                success, msg = future.result()
                pbar.write(msg if success else f"Error: {msg}")
                pbar.update(1)


if __name__ == "__main__":
    folder_path = (
        "/Users/omchavan/Documents/projects/reflex_tutorial/insta_pro-jan-2025"
    )
    convert_media(folder_path, "both")
