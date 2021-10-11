from os import environ

import connexion
from flask_cors import CORS

from nova_api import create_api_files

print("imports")

debug = environ.get('DEBUG') or '0'
if debug == '0':
    debug = False
elif debug == '1':
    debug = True

APIS = environ.get('APIS') or ''
APIS = [api.strip() for api in APIS.split(',')]
print("reading Apis: ", APIS)

VERSION = environ.get('VERSION') or '1'

# Create the application instance
app = connexion.App(__name__, specification_dir=".")
CORS(app.app)
print("App and Cors")

for api in APIS:
    if api == '':
        continue
    app.add_api(api)
    print("Done adding api {api}".format(api=api))
print("Full setup")

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=debug, port=80)
