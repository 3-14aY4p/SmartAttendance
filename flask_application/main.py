from flask import Flask, render_template, Response, jsonify
from CVHandler import generate_frames, get_scan_data

app = Flask(__name__)

