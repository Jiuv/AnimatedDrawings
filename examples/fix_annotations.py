# Copyright (c) 2023-present, FAIR Animated Drawings.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import argparse
from pathlib import Path
import sys
import yaml
from flask import Flask, jsonify, request, send_from_directory
import json
import os

# --- THIS IS THE CRITICAL FIX for cloud environments ---
# It tells the server to be accessible from outside its container.
HOST = '0.0.0.0'
PORT = 5050

# --- Global variable to store the character directory ---
char_anno_dir = ""

# --- Initialize the Flask App ---
# We tell Flask where to find our static files (JS, CSS)
app = Flask(__name__, static_folder='examples/fixer_app')


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
    # The 'static_folder' setting above automatically handles serving the JS and CSS
    return send_from_directory('examples/fixer_app', 'index.html')

@app.route('/annotations', methods=['GET', 'POST'])
def annotations():
    """ Handles getting and saving the joint annotation data. """
    if request.method == 'GET':
        skeleton_data = create_default_skeleton()
        return jsonify(skeleton_data)
    if request.method == 'POST':
        # Make sure the directory exists before writing
        os.makedirs(char_anno_dir, exist_ok=True)
        with open(Path(char_anno_dir, 'char_cfg.yaml'), 'w') as f:
            yaml.dump(request.json, f)
        print(f'Annotations saved to {char_anno_dir}')
        return jsonify({'success': True})

@app.route('/texture.png')
def texture():
    """ Serve the character texture.png file. """
    # This route specifically finds and serves the character image.
    return send_from_directory(char_anno_dir, 'texture.png')

def main(char_anno_dir_in: str):
    """ Main function to start the Flask web server. """
    global char_anno_dir
    char_anno_dir = char_anno_dir_in

    if not os.path.isdir(char_anno_dir):
        print(f'Error: Annotation directory not found at {char_anno_dir}')
        sys.exit(1)

    print("\n--- SERVER IS RUNNING ---")
    print(f"--- Open the 'PORTS' tab in the terminal panel below. ---")
    print(f"--- Find port 5050 and click the 'Open in Browser' icon (a globe). ---")
    
    app.run(host=HOST, port=PORT, debug=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('char_anno_dir', type=str)
    args = parser.parse_args()
    main(args.char_anno_dir)