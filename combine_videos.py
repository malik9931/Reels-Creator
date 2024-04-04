import random
import os
from moviepy.editor import VideoFileClip, clips_array
from multiprocessing import Pool

# Specify the path to the "MotivationVid" folder
motivation_folder = 'MotivationVid/'

# List all motivation video files in the folder
motivation_files = [f for f in os.listdir(motivation_folder) if f.endswith('.mp4')]

# Load the exercise video without resizing
exercise_video = VideoFileClip('exercise.mp4')

# Calculate the duration of the exercise video
exercise_duration = exercise_video.duration

# Specify the output directory path
output_directory = 'results/'

# Create the results folder if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Define the dimensions for the TikTok video while maintaining TikTok's aspect ratio (9:16)
tiktok_width = 1080
tiktok_height = 1920

# Set the fixed height for the motivation video
motivation_height = 1344

# Set the fixed height for the exercise video
exercise_height = 576

# Calculate the width for the exercise video to fit TikTok dimensions
# exercise_width = int(exercise_height * (tiktok_width / tiktok_height))

# Crop the exercise video to achieve a final width of 1080 pixels
exercise_video = exercise_video.resize(width=1080)

# Function to process a single motivation video
def process_motivation_video(motivation_file):
    motivation_video_path = os.path.join(motivation_folder, motivation_file)

    # Get the duration of the motivation video
    motivation_duration = VideoFileClip(motivation_video_path).duration

    # Ensure the motivation video duration does not exceed the exercise video duration
    if motivation_duration <= exercise_duration:
        # Calculate the maximum starting point for the random period
        max_start_time = exercise_duration - motivation_duration

        # Choose a random starting point
        start_time = random.uniform(0, max_start_time)

        # Extract a portion of the exercise video with the same duration as the motivation video
        exercise_video_portion = exercise_video.subclip(start_time, start_time + motivation_duration)

        # Load the motivation video and resize it to 1080x1344 while maintaining aspect ratio
        motivation_video = VideoFileClip(motivation_video_path)
        motivation_video = motivation_video.resize(width=1080)
        motivation_video = motivation_video.set_position(("center", "top"))

        # Calculate the amount to crop from the bottom
        crop_bottom = motivation_video.h - motivation_height

        # Crop the motivation video to the specified height
        motivation_video = motivation_video.crop(y2=motivation_video.h - crop_bottom)

        # Resize the exercise video portion to have a fixed height of 576 pixels
        exercise_video_portion = exercise_video_portion.resize(height=exercise_height)

        # Create a clips array with the motivation video in the upper part and the exercise video portion in the lower part
        final_video = clips_array([[motivation_video], [exercise_video_portion.set_position(("center", "bottom"))]])

        # Create an output file name based on the motivation video file name
        output_file_name = f"combined_{motivation_file}"

        # Specify the output file path
        output_file_path = os.path.join(output_directory, output_file_name)

        # Save the final video in the results folder
        final_video.write_videofile(output_file_path, fps=30, codec="libx264")

    else:
        print(f"Skipping {motivation_file} because its duration exceeds exercise video duration")

if __name__ == "__main__":
    # Use multiprocessing to process motivation videos in parallel
    with Pool(processes=os.cpu_count()) as pool:
        pool.map(process_motivation_video, motivation_files)
