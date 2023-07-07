from django.shortcuts import render
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


uri = "mongodb+srv://alexkai03:fDiGRgzlwU0MFS0V@cluster0.bdepqww.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['sample_airbnb']
collection = db.listingsAndReviews

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

def index(request):
    documents = collection.find({}, {'_id': 0, 'name': 1}).limit(5)
    names = [document['name'] for document in documents]
    return HttpResponse('<br>'.join(names))

def main(request):
    return render(request, 'master.html')