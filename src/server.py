from os import environ

import connexion
import requests
from flask_cors import CORS
import nova_api

debug = environ.get('DEBUG') or '0'
if debug == '0':
    nova_api.DEBUG = False
elif debug == '1':
    nova_api.DEBUG = True

APIS = environ.get('APIS') or ''
APIS = [api.strip() for api in APIS.split(',')]
print("reading Apis: ", APIS)

# Create the application instance
app = connexion.App(__name__, specification_dir=".")
CORS(app.app)
print("App and Cors")

for api in APIS:
    if api == '':
        continue
    app.add_api(api)
    print("Done adding api {api}".format(api=api))


r = requests.get(
    "https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com"
)
if r.ok:
    nova_api.auth.JWT_SECRET = r.json()

print("Full setup")

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=debug, port=5000)
