import os
import time
import subprocess
import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://balok:balok@cluster0.3xvak04.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

database = client["test"]
collection = database["testcoll"]

def save_transcoded_files(dict):
    x = collection.insert_one(dict)
    print(x.inserted_id)


def load_transcoded_files():
    cursor = collection.find()
    transcoded_files = []
    for record in cursor:
        transcoded_files.append(record)
    return transcoded_files

transcoded_files = load_transcoded_files()
print(transcoded_files)


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
            ffmpeg_command = ['ffmpeg', '-i', input_file, '-c:v', 'libx264', '-crf', '18', '-f', 'mpegts', output_file]

            
            # subprocess.run(ffmpeg_command)
            

            # Add the transcoded file to the DB
            dict = {"name": file , "status": "DONE"}

            # Save the updated transcoded files list
            save_transcoded_files(dict)

            # os.remove(input_folder + '/' + file)
            os.remove(os.path.join(input_folder, file))
    
            print (file + ' DONE')
    # Sleep for 5 seconds before checking for new files again
    time.sleep(5)
