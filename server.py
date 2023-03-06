#!/usr/bin/env python3

from flask import Flask, request
from werkzeug.utils import secure_filename

from llama_index import GPTSimpleVectorIndex, download_loader
import json

import secrets


app = Flask(__name__)


@app.route('/index', methods = ['GET', 'POST'])
def upload_and_index():
    if request.method == "POST":
        f = request.files['file']
        filename = f"./uploads/{secure_filename(f.filename)}"
        f.save(filename)

        RDFReader = download_loader('RDFReader')
        document = RDFReader().load_data(file=filename)

        # avoid collisions of filenames
        data_id = secrets.token_hex(15)

        index = GPTSimpleVectorIndex(document)
        index.save_to_disk(f"{data_id}.json")

        return {'id': data_id}


@app.route('/query')
def query():
    args = request.args
    data_id = args.get('id')
    query_str = args.get('query')
    q_index = GPTSimpleVectorIndex.load_from_disk(f"{data_id}.json")

    result = q_index.query(f"{query_str} - return the answer and explanation in a JSON object")
    try:
        json_start = result.response.index('{')
        answer = json.loads(result.response[json_start:])
        answer.update({'success': True})
    except (ValueError, json.JSONDecodeError):
        answer = {'success': False, 'answer': result.response, 'explanation': ''}

    return json.dumps(answer)


@app.route('/')
def hello():
    return 'Hello, World!'


def run_app():
    app.run(host='0.0.0.0', port=5050)


if __name__ == '__main__':
    run_app()
