import argparse
from pathlib import Path
import sys
import yaml
from flask import Flask, jsonify, request, send_from_directory, render_template
import os

# --- THIS IS THE CRITICAL FIX ---
# Since Gunicorn is now running from inside the 'examples' folder,
# the paths to our UI and character folders are now much simpler.
_template_folder = 'fixer_app'
_static_folder = 'fixer_app'
_character_folder = 'drawings'

app = Flask(__name__, template_folder=_template_folder, static_folder=_static_folder)


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
    """ Serve the main HTML file. """
    return render_template('index.html')

@app.route('/annotations', methods=['GET', 'POST'])
def annotations():
    """ Handles getting the default skeleton and saving the user's rig. """
    if request.method == 'GET':
        return jsonify(create_default_skeleton())
    if request.method == 'POST':
        os.makedirs(_character_folder, exist_ok=True)
        with open(Path(_character_folder, 'char_cfg.yaml'), 'w') as f:
            yaml.dump(request.json, f)
        print(f'Annotations saved to {_character_folder}')
        return jsonify({'success': True})

@app.route('/texture.png')
def texture():
    """ Serve the character's texture.png file. """
    return send_from_directory(_character_folder, 'texture.png')