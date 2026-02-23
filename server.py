#!/usr/bin/env python3
"""v86 Control Panel server — static files + state save/restore API."""
import os, gzip
from flask import Flask, request, send_from_directory, jsonify, Response

app = Flask(__name__, static_folder='.', static_url_path='')
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max upload
STATES_DIR = os.path.join(os.path.dirname(__file__), 'states')
os.makedirs(STATES_DIR, exist_ok=True)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/states/<profile>', methods=['GET'])
def get_state(profile):
    path = os.path.join(STATES_DIR, f'{profile}.bin.gz')
    if not os.path.exists(path):
        return '', 404
    with open(path, 'rb') as f:
        data = f.read()
    return Response(data, mimetype='application/octet-stream',
                    headers={'Content-Encoding': 'gzip',
                             'Content-Length': str(len(data))})

@app.route('/api/states/<profile>', methods=['PUT'])
def put_state(profile):
    data = request.get_data()
    if not data:
        return jsonify(error='empty body'), 400
    compressed = gzip.compress(data, compresslevel=1)
    path = os.path.join(STATES_DIR, f'{profile}.bin.gz')
    with open(path, 'wb') as f:
        f.write(compressed)
    raw_mb = len(data) / 1024 / 1024
    gz_mb = len(compressed) / 1024 / 1024
    return jsonify(ok=True, raw_mb=round(raw_mb, 1), compressed_mb=round(gz_mb, 1))

@app.route('/api/states/<profile>', methods=['DELETE'])
def delete_state(profile):
    path = os.path.join(STATES_DIR, f'{profile}.bin.gz')
    if os.path.exists(path):
        os.remove(path)
    return jsonify(ok=True)

@app.route('/api/states', methods=['GET'])
def list_states():
    states = {}
    for f in os.listdir(STATES_DIR):
        if f.endswith('.bin.gz'):
            name = f.replace('.bin.gz', '')
            size = os.path.getsize(os.path.join(STATES_DIR, f))
            states[name] = round(size / 1024 / 1024, 1)
    return jsonify(states)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8087)
