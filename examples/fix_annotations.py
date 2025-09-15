import argparse
from pathlib import Path
import sys
import yaml
from flask import Flask, jsonify, request, send_from_directory, render_template
import os

# --- Global variable to store the character directory ---
char_anno_dir = ""

# --- Initialize the Flask App ---
# We tell Flask where our HTML/JS/CSS files are.
app = Flask(__name__, template_folder='fixer_app', static_folder='fixer_app')

# Set a global variable for the character directory based on startup arguments
# This is a workaround to get the command-line argument into the app
# Gunicorn doesn't pass command-line args in the same way.
# We will read it from an environment variable set by the Dockerfile's CMD, but for now this is simpler.
# A better solution would involve setting env vars. For now, this is hardcoded.
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
    # Using render_template is the standard way to serve the main page
    return render_template('index.html')

@app.route('/annotations', methods=['GET', 'POST'])
def annotations():
    """ Handles getting and saving the joint annotation data. """
    if request.method == 'GET':
        return jsonify(create_default_skeleton())
    if request.method == 'POST':
        os.makedirs(char_anno_dir, exist_ok=True)
        with open(Path(char_anno_dir, 'char_cfg.yaml'), 'w') as f:
            yaml.dump(request.json, f)
        print(f'Annotations saved to {char_anno_dir}')
        return jsonify({'success': True})

@app.route('/texture.png')
def texture():
    """ Serve the character texture.png file. """
    return send_from_directory(char_anno_dir, 'texture.png')

# We no longer need the main() function or the app.run() call,
# because Gunicorn is now our server.