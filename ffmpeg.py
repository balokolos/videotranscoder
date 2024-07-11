import os
import time
import subprocess
import json

def save_transcoded_files(transcoded_files):
    with open('transcoded_files.json', 'w') as f:
        json.dump(transcoded_files, f)

def load_transcoded_files():
    with open('transcoded_files.json', 'r') as f:
        transcoded_files = json.load(f)
    return transcoded_files

input_folder = 'C:/Users/abrafit/Desktop/playground/inputs'
output_folder = 'C:/Users/abrafit/Desktop/playground/done'

# Load the transcoded files from the JSON file
transcoded_files = load_transcoded_files()


while True:
    print ('Checking the asset')
    time.sleep(5)
    # Scan the input folder for new MXF files
    for file in os.listdir(input_folder):
        if file.endswith('.mxf') and file not in transcoded_files:
            # Transcode the MXF file to H.264
            input_file = os.path.join(input_folder, file)
            base, _ = os.path.splitext(file)
            output_file = os.path.join(output_folder, base + '.ts')
            #output_file = os.path.join(output_folder, file + '.mp4')
            ffmpeg_command = ['ffmpeg', '-i', input_file, '-c:v', 'libx264', '-crf', '18', '-f', 'mpegts', output_file]

            
            subprocess.run(ffmpeg_command)

            # Add the transcoded file to the list
            transcoded_files.append(file)

            # Save the updated transcoded files list
            save_transcoded_files(transcoded_files)

            # os.remove(input_folder + '/' + file)
            os.remove(os.path.join(input_folder, file))
    
            print (file + ' DONE')
    # Sleep for 5 seconds before checking for new files again
    time.sleep(5)
