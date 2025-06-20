from flask import Flask, render_template, request, jsonify, send_file
from datetime import datetime
import os
import ssl
import subprocess
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate/<int:days>')
def generate_certificate(days):
    try:
        # Ensure directories exist
        os.makedirs('certs', exist_ok=True)
        
        # Full paths
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'openssl.cnf')
        cert_path = os.path.join(os.path.dirname(__file__), '..', 'certs')
        
        # Generate private key
        key_cmd = f'openssl genrsa -out {os.path.join(cert_path, "server.key")} 2048'
        process = subprocess.Popen(key_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, stderr = process.communicate()
        
        if process.returncode != 0:
            return jsonify({'error': f'Key generation failed: {stderr.decode()}'}), 500
            
        # Generate certificate
        cert_cmd = f'openssl req -x509 -new -nodes -key {os.path.join(cert_path, "server.key")} ' \
                  f'-config {config_path} -sha256 -days {days} ' \
                  f'-out {os.path.join(cert_path, "server.crt")}'
        
        process = subprocess.Popen(cert_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, stderr = process.communicate()
        
        if process.returncode != 0:
            return jsonify({'error': f'Certificate generation failed: {stderr.decode()}'}), 500
            
        return jsonify({'message': 'Certificate generated successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)