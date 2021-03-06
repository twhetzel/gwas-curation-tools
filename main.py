# This work is based on the Google Cloud tutorial
# [processing images asynchronously using Cloud Run](https://cloud.google.com/run/docs/tutorials/image-processing).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
from flask import Flask, request
import json
import os
import sys
import pdfminerDevelop.convert_pdf_to_text as fl

app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    print(f'Starting PubSub process...')
    envelope = request.get_json()
    if not envelope:
        msg = 'no Pub/Sub message received'
        print(f'error: {msg}')
        return f'Bad Request: {msg}', 400

    if not isinstance(envelope, dict) or 'message' not in envelope:
        msg = 'invalid Pub/Sub message format'
        print(f'error: {msg}')
        return f'Bad Request: {msg}', 400

    # Decode the Pub/Sub message.
    pubsub_message = envelope['message']

    print(f'Hello from PubSub!')

    # Flush the stdout to avoid log buffering.
    sys.stdout.flush()
    return ('', 204)

    if isinstance(pubsub_message, dict) and 'data' in pubsub_message:
        try:
            print(f'Trying to get data...')
            data = json.loads(
                base64.b64decode(pubsub_message['data']).decode())

        except Exception as e:
            msg = ('Invalid Pub/Sub message: '
                   'data property is not valid base64 encoded JSON')
            print(f'error: {e}')
            return f'Bad Request: {msg}', 400

        # Validate the message is a Cloud Storage event.
        if not data["name"] or not data["bucket"]:
            msg = ('Invalid Cloud Storage notification: '
                   'expected name and bucket properties')
            print(f'error: {msg}')
            return f'Bad Request: {msg}', 400

        try:
            print(f'Calling get_ancestries...')
            fl.get_ancestries(data)

            # Flush the stdout to avoid log buffering.
            sys.stdout.flush()
            return ('', 204)

        except Exception as e:
            print(f'error: {e}')
            return ('', 500)

    print(f'ERROR: Something went wrong...')
    return ('', 500)


if __name__ == '__main__':
    PORT = int(os.getenv('PORT')) if os.getenv('PORT') else 8080

    # This is used when running locally. Gunicorn is used to run the
    # application on Cloud Run. See entrypoint in Dockerfile.
    app.run(host='127.0.0.1', port=PORT, debug=True)
