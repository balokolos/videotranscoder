import os
import time
import subprocess
import pymongo
import logging
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Connect to MongoDB
uri = "mongodb+srv://balok:balok@cluster0.3xvak04.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
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

def check_input_file(file):
    if not file.endswith('.mxf'):
        raise ValueError(f'Error: {file} is not an mxf file')

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
                    check_input_file(input_files) # will not do anything, just to test exception raise.
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
        except ValueError as e:
            print(f"File not type mxf: {e}")
            
        finally:
            logging.info('Waiting for 10 seconds before next check...')
            time.sleep(10)

if __name__ == "__main__":
    main()