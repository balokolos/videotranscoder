import os
import time
import subprocess
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://balok:balok@cluster0.3xvak04.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

database = client["test"]
collection = database["testcoll"]

def save_transcoded_files(dict):
    x = collection.insert_one(dict)
    msg = f"{dict["name"]} = DONE; ID = {x.inserted_id}"
    print(msg)


def load_transcoded_files():
    cursor = collection.find()
    transcoded_files = []
    for record in cursor:
        transcoded_files.append(record["name"])
    return transcoded_files



input_folder = 'C:/Users/abrafit/Desktop/playground/inputs'
output_folder = 'C:/Users/abrafit/Desktop/playground/done'


while True:
    print ('Checking the asset')
    # Load the transcoded files from the JSON file
    transcoded_files = load_transcoded_files()
    time.sleep(2)
    # Scan the input folder for new MXF files
    try:
        file = None
        for file in os.listdir(input_folder):
            if file.endswith('.mxf') and file not in transcoded_files:
                # Transcode the MXF file to H.264
                input_file = os.path.join(input_folder, file)
                base, _ = os.path.splitext(file)
                output_file = os.path.join(output_folder, base + '.ts')
                ffmpeg_command = ['ffmpeg', '-i', input_file, '-c:v', 'libx264', '-crf', '18', '-f', 'mpegts', output_file]
                print(file)

                # subprocess.run(ffmpeg_command)
                subprocess.run(ffmpeg_command)
                        
    except subprocess.CalledProcessError as e:
        print(f"Error executing ffmpeg command: {e}")
                        
    except pymongo.errors.PyMongoError as e:
        print(f"MongoDB error: {e}")
                        
    except Exception as e:
        print(f"Unexpected error occurred: {e}")


    except FileNotFoundError as e:
        print(f"File not found error: {e}")

    finally:
        if file not in transcoded_files:
            # Add the transcoded file to the DB
            dict = {"name": file , "status": "DONE"}
            # Save the updated transcoded files list
            save_transcoded_files(dict)
            # os.remove(input_folder + '/' + file)
            os.remove(os.path.join(input_folder, file))
        elif file is None:
            print(f"{file} new file to process")
        else:
            print(f"{file} already exist")