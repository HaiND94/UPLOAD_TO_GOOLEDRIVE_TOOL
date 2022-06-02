from flask import Flask
from flask import request
import requests
import json
import sys
import logging

logging.basicConfig(level="INFO")


# CONSTANT
CHUNK_SIZE = 3 * 1024 * 1024
accessToken = \
    'ya29.a0ARrdaM-1a8ijur6FJhHbPohc6Vj7fgTHPJ5q7MhA2SDVLt-ZKLNMNqBm_I-Nx5n2G4lMFZOdZ8hHv8-fZJpeigsCDVCD6TGXcpAzHSIA6qHY0bQr3ilIQUtflnBfTzaoqk9np9v4g_MB8A7SO9rWBkiwLG9M'
app = Flask(__name__)


@app.route("/upload", methods=['POST'])
def upload():
    logging.info("Recived request from client")
    if request.method == "POST":
        count = 0
        upload_file = request.files['file']
        # Connect to google api
        headers = {'Authorization': 'Bearer ' + accessToken,
                   'Content-Type': 'application/json'}
        parameters = {'name': 'test.jpg',
                      'description': 'This is test image',
                      'parents': ["1K_FgmfBYptMN9pHay0aQB-T3w07AE7hJ"]}
        r = \
            requests.post('https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable'
                          , headers=headers, data=json.dumps(parameters))
        location = r.headers['location']
        end_status = False
        end_file = 0
        with open("result.jpg", "bw") as f:
        
            while True:
                chunk = upload_file.stream.read(CHUNK_SIZE)
                f.write(chunk)
                chunk_size = len(chunk)
                end_file += chunk_size

                logging.info("----------------------------------------------------")
                logging.info(f"Size of Received Chunk From Client:  {chunk_size}")
                logging.info("----------------------------------------------------")
                if chunk_size < CHUNK_SIZE:
                    headers = {'Content-Length': str(chunk_size),
                               'Content-Range': 'bytes ' + str(count * CHUNK_SIZE)\
                                                + '-' + str(end_file - 1) + '/' + str(end_file)}
                    end_status = True
                else:
                    finalByte = (count + 1) * CHUNK_SIZE - 1
                    headers = {'Content-Length': str(chunk_size),
                               'Content-Range': 'bytes ' + str(CHUNK_SIZE * count)\
                                                + '-' + str(finalByte) + '/*'}
                r = requests.put(location, headers=headers, data=chunk)
                logging.info(r.text)  # Response
                count += 1
                if end_status:
                    break
    else:
        return "Method not allow", 405

    return "ok", 200


if __name__ == "__main__":
    app.run(debug=True)


