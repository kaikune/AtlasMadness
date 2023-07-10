from django.shortcuts import render
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from django.http import HttpResponse
from django.shortcuts import render
import vertexai
from vertexai.preview.language_models import CodeGenerationModel
from django.views.decorators.csrf import csrf_exempt
import ast
import re

uri = 'mongodb+srv://alexkai03:fDiGRgzlwU0MFS0V@cluster0.bdepqww.mongodb.net/?retryWrites=true&w=majority'

# TODO: Make updatable
prompt = 'You are a natural language to MongoDB query generator that only outputs code if 100percent certain of correctness.\
      Assume prerequisite code is supplied. All queries will be executed in python so it must follow python syntax. \
      In the format: \
    db=client["database_name"] \
    collection = db.collection_name \
    #Do the mongoDB query here \
    cursor = #query result \
    The constraints are: \
    The database name is "sample_airbnb". \
    The collection is "listingsAndReviews". \
    There is a limit of 10 documents unless otherwise specified. \
    Instead of printing the result, store the result in cursor. \
    Write the query: "{}"'

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['sample_airbnb']
collection = db.listingsAndReviews


# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print('Successfully connected to MongoDB Atlas!')
except Exception as e:
    print(e)

# Checks for valid python code
def isValidPython(code):
   print('Validating python code...')
   try:
       ast.parse(code)
   except SyntaxError:
       return False
   return True

# Generate query from user input
def generateQuery(str):
    print('Generating query...')
    vertexai.init(project='atlas-madness-392102', location='us-central1')
    parameters = {
        'temperature': 0.2,
        'max_output_tokens': 1024
    }
    model = CodeGenerationModel.from_pretrained('code-bison@001')
    response = model.predict(
        prefix = str,
        **parameters
    )
    response = response.text[9:-3]
    print(f'Response from Model:\n{response}')

    if not isValidPython(response):
        raise Exception('Invalid code generated')
    return response

cursor = 'Cursor Empty'

# Attempt to run generated query
def runQuery(query):
    print('Running query...')
    try:
        exec(query, globals())
        return cursor
    except Exception as e:
        print(f'Invalid query: {e}')
        return 'Bad query'

# def index(request):
#     return HttpResponse(runQuery(generateQuery(prompt)))
#     # documents = collection.find({}, {'_id': 0, 'name': 1}).limit(5)
#     # names = [document['name'] for document in documents]
#     # return HttpResponse('<br>'.join(names))

@csrf_exempt
def main(request):
    userQuery = ''
    if request.method == 'POST':
        # Retrieve the userQuery value from the form data
        userQuery = request.POST.get('userQuery', '') 

        print('User Query:', userQuery)
        userQuery = prompt.format(userQuery)
        result = generateQuery(userQuery)
        # You can perform further processing with the userQuery value here
    else:
        userQuery = ''  # Set the initial value of userQuery when the page is first loaded
        result = None

    context = {'userQuery': userQuery, 'result': result}
    return render(request, 'master.html', context)

