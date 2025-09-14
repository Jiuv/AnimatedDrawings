# Copyright (c) 2023-present, FAIR Animated Drawings.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import argparse
import webbrowser
from pathlib import Path
import sys
import yaml
from flask import Flask, jsonify, request, send_from_directory, send_file
import json
import os

# Create a default skeleton structure.
# This function replaces the need to load an existing file.
def create_default_skeleton():
    """
    Returns a dictionary containing a default skeleton structure and joints.
    All joints are initialized at position [0, 0].
    """
    return {
        'skeleton': [
            {'name': 'hip', 'parent': ''},
            {'name': 'neck', 'parent': 'hip'},
            {'name': 'nose', 'parent': 'neck'},
            {'name': 'l_shoulder', 'parent': 'neck'},
            {'name': 'l_elbow', 'parent': 'l_shoulder'},
            {'name': 'l_wrist', 'parent': 'l_elbow'},
            {'name': 'r_shoulder', 'parent': 'neck'},
            {'name': 'r_elbow', 'parent': 'r_shoulder'},
            {'name': 'r_wrist', 'parent': 'r_elbow'},
            {'name': 'l_hip', 'parent': 'hip'},
            {'name': 'l_knee', 'parent': 'l_hip'},
            {'name': 'l_ankle', 'parent': 'l_knee'},
            {'name': 'r_hip', 'parent': 'hip'},
            {'name': 'r_knee', 'parent': 'r_hip'},
            {'name': 'r_ankle', 'parent': 'r_knee'}
        ],
        'joints': {
            'hip': [0, 0], 'neck': [0, 0], 'nose': [0, 0],
            'l_shoulder': [0, 0], 'l_elbow': [0, 0], 'l_wrist': [0, 0],
            'r_shoulder': [0, 0], 'r_elbow': [0, 0], 'r_wrist': [0, 0],
            'l_hip': [0, 0], 'l_knee': [0, 0], 'l_ankle': [0, 0],
            'r_hip': [0, 0], 'r_knee': [0, 0], 'r_ankle': [0, 0]
        }
    }

# The host and port the Flask app will run on
HOST = '127.0.0.1'
PORT = 5050

# The directory where the user's character files will be.
# We will modify this later to handle different users.
char_anno_dir = ""


# Initialize the Flask app
app = Flask(__name__)


@app.route('/')
def index():
    """
    Serve the main HTML file for the rigging interface.
    """
    # We will create the actual HTML file in the next step.
    # For now, this points to a non-existent file.
    return send_from_directory('fixer_app', 'index.html')


@app.route('/annotations', methods=['GET', 'POST'])
def annotations():
    """
    Handles getting and saving the joint annotation data.
    """
    if request.method == 'GET':
        # When the page loads, send it the default skeleton we created
        skeleton_data = create_default_skeleton()
        return jsonify(skeleton_data)

    if request.method == 'POST':
        # When the user hits "Submit", save the new joint data
        with open(Path(char_anno_dir, 'char_cfg.yaml'), 'w') as f:
            yaml.dump(request.json, f)
        print(f'Annotations saved to {char_anno_dir}')
        return jsonify({'success': True})


@app.route('/<path:filename>')
def serve_static(filename):
    """
    Serve static files (like the character image) from the annotation directory.
    """
    return send_from_directory(char_anno_dir, filename, as_attachment=False)


def main(char_anno_dir_in: str):
    """
    Main function to start the Flask web server.
    """
    global char_anno_dir
    char_anno_dir = char_anno_dir_in

    # Basic check to make sure the provided directory exists
    if not os.path.isdir(char_anno_dir):
        print(f'Error: Annotation directory not found at {char_anno_dir}')
        sys.exit(1)

    # Automatically open the user's web browser to the correct page
    webbrowser.open(f'http://{HOST}:{PORT}')

    # Run the app
    app.run(host=HOST, port=PORT, debug=True)


if __name__ == '__main__':
    # We will change how this is called later.
    # For now, it's set up to work similarly to the original script.
    parser = argparse.ArgumentParser()
    parser.add_argument('char_anno_dir', type=str)
    args = parser.parse_args()

    main(args.char_anno_dir)