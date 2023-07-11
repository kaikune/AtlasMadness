from django.shortcuts import render
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from django.http import JsonResponse
from django.shortcuts import render
import vertexai
from vertexai.preview.language_models import CodeGenerationModel
from django.views.decorators.csrf import csrf_exempt
import ast
import pandas as pd


uri = 'mongodb+srv://alexkai03:fDiGRgzlwU0MFS0V@cluster0.bdepqww.mongodb.net/?retryWrites=true&w=majority'

# TODO: Make updatable
prompt = 'You are a natural language to MongoDB query generator that only outputs code if 100percent certain of correctness.\
      Assume prerequisite code is supplied. All queries will be executed in python so it must follow python syntax. \
      In the format: \
    db=client["{}"] \
    collection = db.{} \
    #Do the mongoDB query here \
    cursor = #query result \
    The constraints are: \
    The database name is "sample_supplies". \
    The collection is "sales". \
    There is a limit of 10 documents unless otherwise specified. \
    Instead of printing the result, store the result in cursor. \
    Write the query: "{}"'

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# db = client['sample_supplies']
# collection = db.sales


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
   print('Validated!')
   return True

# Generate query from user input
def generateQuery(str):
    print('Generating query...')
    vertexai.init(project='atlas-madness-392102', location='us-central1')
    parameters = {
        'temperature': 0.1,
        'max_output_tokens': 1024
    }
    model = CodeGenerationModel.from_pretrained('code-bison@001')
    response = model.predict(
        prefix = str,
        **parameters
    )
    response = response.text[9:-3]
    print(f'Response from Model:\n{response}')
    return response

cursor = 'Cursor Empty'

# Attempt to run generated query
def runQuery(query, db, collection):
    def runQueryHelper():
        nonlocal db, collection
        print('Running query...')
        try:
            exec(query, globals())
            print('Query execute')
            return cursor
        except Exception as e:
            print(f'Invalid query: {e}')
            return 'Bad query'
    return runQueryHelper()


@csrf_exempt
def main(request):
    userQuery = ''
    data = ''
    df = None
    db = None
    databaseNames = client.list_database_names()
    if request.method == 'POST':
        # Retrieve the userQuery value from the form data
        userQuery = request.POST.get('userQuery', '') 
        db = request.POST.get('database')
        collection = request.POST.get('collection')

        collectionNames = []
        if db:
            # Get the list of collections for the selected database
            collectionNames = client[db].list_collection_names()

        userQuery = prompt.format(db, collection, userQuery)
        print('User Query:', userQuery)
        result = generateQuery(userQuery)

        if isValidPython(result):
            data = runQuery(result, db, collection)
            df = pd.DataFrame(data)
            print(df)
            df = df.to_html(classes='table table-dark table-hover')
        else:
            print('Bad python generated')

        context = {
            'userQuery': userQuery,
            'result': result, 
            'dataframe': df, 
            'databaseNames': databaseNames, 
            'collectionNames': collectionNames,
            'selectedDB': db,
            'selectedCollection': collection
        }
    else:
        userQuery = ''  # Set the initial value of userQuery when the page is first loaded
        result = '' 
        context = {'databaseNames': databaseNames, 'userQuery': userQuery, 'result': result}

    return render(request, 'master.html', context)

@csrf_exempt
def update_collections(request):
    db = request.POST.get('database')
    collectionNames = []
    if db:
        # Get the list of collections for the selected database
        collectionNames = client[db].list_collection_names()

    return JsonResponse({'collections': collectionNames})
