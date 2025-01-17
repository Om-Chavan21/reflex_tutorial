VIDEO_EXTENSIONS = [
    ".mp4",  # MPEG-4 Part 14
    ".avi",  # Audio Video Interleave
    ".mov",  # QuickTime Movie
    ".mkv",  # Matroska Video
    ".wmv",  # Windows Media Video
    ".flv",  # Flash Video
    ".webm",  # Web Media
    ".m4v",  # MPEG-4
    ".3gp",  # 3GPP
    ".mpg",  # MPEG-1
    ".mpeg",  # MPEG
    ".m2v",  # MPEG-2
    ".ogv",  # Ogg Video
    ".mts",  # AVCHD
    ".ts",  # MPEG Transport Stream
    ".vob",  # DVD Video Object
]

"""
List of common video file extensions.
Can be used to filter or validate video files.
All extensions include the leading dot.
"""
import subprocess
import concurrent.futures
from pathlib import Path
from tqdm import tqdm
import shutil


def convert_single_video(file_path: Path, output_folder: Path) -> tuple[bool, str]:
    """Convert a single video to MP4 using ffmpeg or copy if already MP4"""
    try:
        output_path = output_folder / f"{file_path.stem}.mp4"

        # If already MP4, just copy
        if file_path.suffix.lower() == ".mp4":
            shutil.move(file_path, output_path)
            return True, f"Copied MP4: {file_path.name}"

        # Otherwise convert using ffmpeg
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
        file_path.unlink()  # Delete original only for non-MP4 files
        return True, f"Converted: {file_path.name}"
    except subprocess.CalledProcessError as e:
        return False, f"Error converting {file_path.name}: {e.stderr.decode()}"
    except shutil.Error as e:
        return False, f"Error copying {file_path.name}: {str(e)}"


def convert_videos_to_mp4(input_folder: str, max_workers: int = 4):
    """
    Converts all supported video files to MP4 format using ffmpeg.
    Uses parallel processing for better performance.
    """
    input_path = Path(input_folder)
    output_folder = input_path / "MP4_CONVERTED"
    output_folder.mkdir(exist_ok=True)

    # Find all eligible video files
    video_files = [
        f
        for f in input_path.rglob("*")
        if f.suffix.lower() in VIDEO_EXTENSIONS and "MP4_CONVERTED" not in str(f)
    ]

    if not video_files:
        print("No videos found to convert")
        return

    # Convert videos in parallel with progress bar
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(convert_single_video, f, output_folder) for f in video_files
        ]

        with tqdm(total=len(video_files), desc="Converting videos") as pbar:
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
    convert_videos_to_mp4(folder_path)
