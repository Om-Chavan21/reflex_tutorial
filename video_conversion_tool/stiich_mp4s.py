import os
import subprocess
import json


def get_video_resolution(file_path):
    """Get resolution of a video file using ffprobe."""
    cmd = [
        "ffprobe",
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width,height",
        file_path,
    ]

    try:
        output = subprocess.check_output(cmd)
        data = json.loads(output)
        width = int(data["streams"][0]["width"])
        height = int(data["streams"][0]["height"])
        return (width, height)
    except Exception as e:
        return None


def get_all_video_resolutions(directory):
    """Get resolutions of all MP4 files in the directory."""
    resolutions = []

    # Check if directory exists
    if not os.path.exists(directory):
        return ["Directory not found"]

    # Get all MP4 files
    mp4_files = [f for f in os.listdir(directory) if f.lower().endswith(".mp4")]

    # Get resolution for each file
    for file in mp4_files:
        full_path = os.path.join(directory, file)
        resolution = get_video_resolution(full_path)
        resolutions.append(f"{file}: {resolution}")

    return resolutions


def find_largest_dimensions(directory):
    """Find videos with largest width and height."""
    max_width = 0
    max_height = 0
    max_width_file = ""
    max_height_file = ""

    for file in os.listdir(directory):
        if file.lower().endswith(".mp4"):
            full_path = os.path.join(directory, file)
            dimensions = get_video_resolution(full_path)

            if dimensions:
                width, height = dimensions
                if width > max_width:
                    max_width = width
                    max_width_file = file
                if height > max_height:
                    max_height = height
                    max_height_file = file

    return {
        "largest_width": {"file": max_width_file, "width": max_width},
        "largest_height": {"file": max_height_file, "height": max_height},
    }


# Directory path
directory = "/Users/omchavan/Documents/projects/reflex_tutorial/video_conversion_tool/insta_pro-jan-2025/MP4_CONVERTED"

# Get and print resolutions
resolutions = get_all_video_resolutions(directory)
for res in resolutions:
    print(res)

# Find and print largest dimensions
largest = find_largest_dimensions(directory)
print("\nLargest dimensions:")
print(
    f"Widest video: {largest['largest_width']['file']} ({largest['largest_width']['width']}px)"
)
print(
    f"Tallest video: {largest['largest_height']['file']} ({largest['largest_height']['height']}px)"
)


def calculate_optimal_dimensions(max_width, max_height):
    """Calculate optimal 16:9 dimensions that fit max width and height."""
    # Calculate minimum width and height needed for 16:9 ratio
    width_from_height = (max_height * 16) // 9
    height_from_width = (max_width * 9) // 16

    # Choose the larger dimensions to ensure all videos fit
    if width_from_height >= max_width:
        return width_from_height, max_height
    else:
        return max_width, height_from_width


# After finding largest dimensions, add:
optimal_width, optimal_height = calculate_optimal_dimensions(
    largest["largest_width"]["width"], largest["largest_height"]["height"]
)

print("\nOptimal 16:9 dimensions that fit all videos:")
print(f"Width: {optimal_width}px")
print(f"Height: {optimal_height}px")
print(f"Ratio: {optimal_width/optimal_height:.2f}:1")


def calculate_optimal_dimensions(max_width, max_height):
    """Find smallest standard resolution that fits the given dimensions."""
    # Standard resolutions (height in pixels)
    STANDARD_HEIGHTS = {
        "144p": 144,
        "240p": 240,
        "360p": 360,
        "480p": 480,
        "720p": 720,
        "1080p": 1080,
        "1440p": 1440,
        "2160p": 2160,
    }

    def get_width_from_height(height):
        """Calculate 16:9 width from height."""
        return (height * 16) // 9

    # Find first resolution that fits both dimensions
    for res_name, height in STANDARD_HEIGHTS.items():
        width = get_width_from_height(height)
        if width >= max_width and height >= max_height:
            return {"resolution": res_name, "width": width, "height": height}

    # If no standard resolution fits, return 4K
    return {"resolution": "2160p", "width": 3840, "height": 2160}


# Update implementation
optimal = calculate_optimal_dimensions(
    largest["largest_width"]["width"], largest["largest_height"]["height"]
)

print("\nOptimal standard resolution that fits all videos:")
print(f"Resolution: {optimal['resolution']}")
print(f"Width: {optimal['width']}px")
print(f"Height: {optimal['height']}px")
print(f"Ratio: {optimal['width']/optimal['height']:.2f}:1")


def create_black_frame_video(width, height, output_path):
    """Create a black frame video of specified dimensions and 4 hours duration at 1fps."""
    try:
        cmd = [
            "ffmpeg",
            "-f",
            "lavfi",
            "-i",
            f"color=c=black:s={width}x{height}",
            "-r",
            "1",  # Set framerate to 1 fps
            "-t",
            "14400",  # 4 hours in seconds
            "-c:v",
            "libx264",
            "-tune",
            "stillimage",
            "-pix_fmt",
            "yuv420p",
            "-y",  # Overwrite output file if exists
            output_path,
        ]

        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating black frame video: {str(e)}")
        return False


# Usage:
output_path = os.path.join(directory, "black_frame_4hours.mp4")
success = create_black_frame_video(optimal["width"], optimal["height"], output_path)

if success:
    print(f"\nCreated black frame video at: {output_path}")
    print(f"Resolution: {optimal['width']}x{optimal['height']}")
else:
    print("Failed to create black frame video")
