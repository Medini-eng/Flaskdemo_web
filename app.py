from flask import Flask, render_template, request, redirect, url_for, send_file
from azure.storage.blob import BlobServiceClient
from io import BytesIO
import os

app = Flask(__name__)

connection_string = "DefaultEndpointsProtocol=https;AccountName=mediniproject;AccountKey=3aRTzwN0XOqdCgidxB+mn4y0Mw1TXSsONhXvXtNeMdxOlnYH7cCsOK9lDglwLvSHtVRSG1oy4Gm1+AStPGVqOg==;EndpointSuffix=core.windows.net"

container_name = "project1"

blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

@app.route('/')
def index():
    blobs = container_client.list_blobs()
    blob_list = []
    for blob in blobs:
        blob_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob.name}"
        blob_list.append({'name': blob.name, 'url': blob_url})
    return render_template('index.html', blobs=blob_list)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        blob_client = container_client.get_blob_client(file.filename)
        blob_client.upload_blob(file, overwrite=True)
    return redirect(url_for('index'))

@app.route('/download/<blob_name>')
def download(blob_name):
    blob_client = container_client.get_blob_client(blob_name)
    blob_data = blob_client.download_blob()
    stream = BytesIO()
    blob_data.readinto(stream)
    stream.seek(0)
    return send_file(stream, download_name=blob_name, as_attachment=True)

if __name__ == '__main__':
#     app.run(debug=True)
      app = app
