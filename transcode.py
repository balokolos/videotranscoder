import subprocess
import os
import argparse

def transcode_to_dash(input_file, output_dir):
    """
    Transcodes an MP4 video file to DASH format using FFmpeg.
    
    Args:
        input_file (str): Path to the input MP4 video file.
        output_dir (str): Directory to save the DASH output files.
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Define the output MPD file path
    output_mpd = os.path.join(output_dir, "manifest.mpd")
    
    # FFmpeg DASH transcoding command
    ffmpeg_command = [
        "ffmpeg",
        "-i", input_file,            # Input file
        "-c:v", "libx264",           # Video codec
        "-c:a", "aac",               # Audio codec
        "-preset", "fast",           # Encoding speed/quality tradeoff
        "-b:v", "1000k",             # Video bitrate
        "-map", "0",                 # Map all streams
        "-f", "dash",                # Output format (DASH)
        output_mpd                   # Output MPD file
    ]
    
    try:
        # Run the FFmpeg command
        subprocess.run(ffmpeg_command, check=True)
        print(f"DASH files have been generated in: {output_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error during transcoding: {e}")

# Example usage
if __name__ == "__main__":
    '''
        input_video = "video/video.mp4"  # Path to your input MP4 file
        output_folder = "dash_output"  # Output directory for DASH files
        transcode_to_dash(input_video, output_folder)
    '''

parser = argparse.ArgumentParser()
parser.add_argument("input_video", type=str, help="Path to the input MP4 video file.")
parser.add_argument("output_video", type=str, help="Path to the dash output.")
args = parser.parse_args()
transcode_to_dash(args.input_video, args.output_video)