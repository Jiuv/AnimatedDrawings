import argparse, sys, yaml, os
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory, render_template

_template_folder = '/app/examples/fixer_app'
_static_folder = '/app/examples/fixer_app'
_character_folder = '/app/examples/drawings'

app = Flask(__name__, template_folder=_template_folder, static_folder=_static_folder)

def create_default_skeleton():
    return { 'skeleton': [ {'name': 'hip', 'parent': ''}, {'name': 'neck', 'parent': 'hip'}, {'name': 'nose', 'parent': 'neck'}, {'name': 'l_shoulder', 'parent': 'neck'}, {'name': 'l_elbow', 'parent': 'l_shoulder'}, {'name': 'l_wrist', 'parent': 'l_elbow'}, {'name': 'r_shoulder', 'parent': 'neck'}, {'name': 'r_elbow', 'parent': 'r_shoulder'}, {'name': 'r_wrist', 'parent': 'r_elbow'}, {'name': 'l_hip', 'parent': 'hip'}, {'name': 'l_knee', 'parent': 'l_hip'}, {'name': 'l_ankle', 'parent': 'l_knee'}, {'name': 'r_hip', 'parent': 'hip'}, {'name': 'r_knee', 'parent': 'r_hip'}, {'name': 'r_ankle', 'parent': 'r_knee'} ], 'joints': { 'hip': [0, 0], 'neck': [0, 0], 'nose': [0, 0], 'l_shoulder': [0, 0], 'l_elbow': [0, 0], 'l_wrist': [0, 0], 'r_shoulder': [0, 0], 'r_elbow': [0, 0], 'r_wrist': [0, 0], 'l_hip': [0, 0], 'l_knee': [0, 0], 'l_ankle': [0, 0], 'r_hip': [0, 0], 'r_knee': [0, 0], 'r_ankle': [0, 0] } }

@app.route('/')
def index(): return render_template('index.html')

@app.route('/annotations', methods=['GET', 'POST'])
def annotations():
    if request.method == 'GET': return jsonify(create_default_skeleton())
    os.makedirs(_character_folder, exist_ok=True)
    with open(Path(_character_folder, 'char_cfg.yaml'), 'w') as f: yaml.dump(request.json, f)
    return jsonify({'success': True})

@app.route('/texture.png')
def texture(): return send_from_directory(_character_folder, 'texture.png')