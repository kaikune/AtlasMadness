
# from google.cloud import aiplatform
# from google.oauth2 import service_account

# API_KEY = 'AIzaSyDHHthSwlkCfUW-pVhhaT9HLoh3s7GxeWU'
# my_credentials = '../credentials.json'

# aiplatform.init(
#     # your Google Cloud Project ID or number
#     # environment default used is not set
#     project='atlas-madness-392102',

#     # the Vertex AI region you will use
#     # defaults to us-central1
#     location='us-central1',

#     # Google Cloud Storage bucket in same region as location
#     # used to stage artifacts
#     staging_bucket='gs://bucket-1025',

#     # custom google.auth.credentials.Credentials
#     # environment default creds used if not set
#     credentials=my_credentials,

#     # customer managed encryption key resource name
#     # will be applied to all Vertex AI resources if set
#     encryption_spec_key_name=my_encryption_key_name,

#     # the name of the experiment to use to track
#     # logged metrics and parameters
#     experiment='my-experiment',

#     # description of the experiment above
#     experiment_description='my experiment decsription'
# )