import argparse
from pathlib import Path
import sys
import yaml
from flask import Flask, jsonify, request, send_from_directory, render_template
import os

# --- THIS IS THE CRITICAL FIX ---
# We determine the project's root directory and then build the paths from there.
# This is the most robust method for any server environment.
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_template_folder = os.path.join(ROOT_DIR, 'examples/fixer_app')
_static_folder = os.path.join(ROOT_DIR, 'examples/fixer_app')

app = Flask(__name__, template_folder=_template_folder, static_folder=_static_folder)

# Hardcode the character directory for now
char_anno_dir = "examples/drawings"


def create_default_skeleton():
    """ Returns a dictionary containing a default skeleton structure. """
    return {
        'skeleton': [
            {'name': 'hip', 'parent': ''}, {'name': 'neck', 'parent': 'hip'},
            {'name': 'nose', 'parent': 'neck'}, {'name': 'l_shoulder', 'parent': 'neck'},
            {'name': 'l_elbow', 'parent': 'l_shoulder'}, {'name': 'l_wrist', 'parent': 'l_elbow'},
            {'name': 'r_shoulder', 'parent': 'neck'}, {'name': 'r_elbow', 'parent': 'r_shoulder'},
            {'name': 'r_wrist', 'parent': 'r_elbow'}, {'name': 'l_hip', 'parent': 'hip'},
            {'name': 'l_knee', 'parent': 'l_hip'}, {'name': 'l_ankle', 'parent': 'l_knee'},
            {'name': 'r_hip', 'parent': 'hip'}, {'name': 'r_knee', 'parent': 'r_hip'},
            {'name': 'r_ankle', 'parent': 'r_knee'}
        ], 'joints': {
            'hip': [0, 0], 'neck': [0, 0], 'nose': [0, 0], 'l_shoulder': [0, 0],
            'l_elbow': [0, 0], 'l_wrist': [0, 0], 'r_shoulder': [0, 0], 'r_elbow': [0, 0],
            'r_wrist': [0, 0], 'l_hip': [0, 0], 'l_knee': [0, 0], 'l_ankle': [0, 0],
            'r_hip': [0, 0], 'r_knee': [0, 0], 'r_ankle': [0, 0]
        }
    }

@app.route('/')
def index():
    """ Serve the main HTML file for the rigging interface. """
    return render_template('index.html')

@app.route('/annotations', methods=['GET', 'POST'])
def annotations():
    """ Handles getting and saving the joint annotation data. """
    if request.method == 'GET':
        return jsonify(create_default_skeleton())
    if request.method == 'POST':
        # This part will still have issues on the server's temp file system,
        # but the main UI will load.
        save_path = os.path.join(ROOT_DIR, char_anno_dir)
        os.makedirs(save_path, exist_ok=True)
        with open(Path(save_path, 'char_cfg.yaml'), 'w') as f:
            yaml.dump(request.json, f)
        print(f'Annotations saved to {save_path}')
        return jsonify({'success': True})

@app.route('/texture.png')
def texture():
    """ Serve the character texture.png file. """
    image_path = os.path.join(ROOT_DIR, char_anno_dir)
    return send_from_directory(image_path, 'texture.png')