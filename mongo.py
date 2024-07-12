from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://balok:balok@cluster0.3xvak04.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

#Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

database = client["test"]
collection = database["testcoll"]
                    
# To find() all the entries inside collection name 'myTable' 
cursor = collection.find()
for record in cursor: 
    print(record) 

