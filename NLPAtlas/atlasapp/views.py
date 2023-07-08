from django.shortcuts import render
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from django.http import HttpResponse
from django.shortcuts import render
import vertexai
from vertexai.preview.language_models import CodeGenerationModel

# Create your views here.

def generateQuery(str):
    vertexai.init(project="atlas-madness-392102", location="us-central1")
    parameters = {
        "temperature": 0.1,
        "max_output_tokens": 1024
    }
    model = CodeGenerationModel.from_pretrained("code-bison@001")
    response = model.predict(
        prefix = str,
        **parameters
    )
    print(f"Response from Model: {response.text}")
    return response.text

uri = "mongodb+srv://alexkai03:fDiGRgzlwU0MFS0V@cluster0.bdepqww.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['sample_airbnb']
collection = db.listingsAndReviews

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Successfully connected to MongoDB Atlas!")
except Exception as e:
    print(e)

def index(request):
    documents = collection.find({}, {'_id': 0, 'name': 1}).limit(5)
    names = [document['name'] for document in documents]
    return HttpResponse('<br>'.join(names))

def main(request):
    return render(request, 'master.html')