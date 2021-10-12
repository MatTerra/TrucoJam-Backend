"""
Server configuration for the backend of Truco JAM
"""
from os import environ

import connexion
import requests
from cryptography.hazmat.bindings._rust.x509 import load_pem_x509_certificate
from cryptography.hazmat.primitives._serialization import Encoding, \
    PublicFormat
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
    certs = r.json()
    for cert_id in certs:
        cert_public_key = load_pem_x509_certificate(certs[cert_id]).public_key()
        certs[cert_id] = cert_public_key.public_bytes(
            encoding=Encoding.PEM,
            format=PublicFormat.SubjectPublicKeyInfo
        )
    nova_api.auth.JWT_SECRET = certs

print("Full setup")

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=debug, port=5000)
