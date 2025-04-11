import os
import time
import subprocess
import pymongo
import logging
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Connect to MongoDB
uri = "<MONGO_URI>"
client = MongoClient(uri, server_api=ServerApi('1'))
database = client["test"]
collection = database["testcoll"]

# Set up logging
logging.basicConfig(filename='videotranscoder.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define input and output directories
input_dir = '/home/balok/play/videotranscoder/in'
output_dir = '/home/balok/play/videotranscoder/out'

def save_transcoded_files(dict):
    x = collection.insert_one(dict)
    msg = f"{dict['name']} = DONE; ID = {x.inserted_id}"
    print(msg)


def load_transcoded_files():
    cursor = collection.find()
    transcoded_files = []
    for record in cursor:
        transcoded_files.append(record["name"])
    return transcoded_files

def main():
    while True:
        print('Checking the asset')
        transcoded_files = set(load_transcoded_files())
        input_files = set(os.listdir(input_dir))
        time.sleep(10)
        try:
            for file in input_files - transcoded_files:
                if file.endswith('.mxf'):
                    input_file = os.path.join(input_dir, file)
                    base, _ = os.path.splitext(file)
                    output_file = os.path.join(output_dir, base + '.ts')
                    ffmpeg_command = [
                        'ffmpeg', '-i', input_file, '-c:v', 'libx264', 
                        '-crf', '18', '-f', 'mpegts', output_file
                    ]
                    logging.info(f'Processing file: {file}')
                    print(file)
                    subprocess.run(ffmpeg_command)
                    save_transcoded_files({"name": file, "status": "Done"})
        except subprocess.CalledProcessError as e:
            logging.error(f'Error executing ffmpeg command: {e}')
            print(f"Error executing ffmpeg command: {e}")
        except pymongo.errors.PyMongoError as e:
            logging.error(f'Unexpected error occurred: {e}')
            print(f"MongoDB error: {e}")
        except Exception as e:
            logging.error(f'File not found error: {e}')
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
                os.remove(os.path.join(input_dir, file))
                logging.info(f'Removed file: {file}')
            elif file is None:
                logging.info(f'No file to process')
                print(f"{file} new file to process")
            else:
                logging.info(f'File already exist: {file}')
                print(f"{file} already exist")

if __name__ == "__main__":
    main()