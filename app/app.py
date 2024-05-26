from flask import Flask, request, render_template, redirect, url_for
from loguru import logger
import json
import os
import subprocess
from handler.version_fetch import update_service_versions  # Import the function

VERSION = '0.1.2'

app = Flask(__name__, template_folder='./templates', static_folder='./frontend/static')

logger.add("app.log", rotation="10 MB", retention="7 days", level="DEBUG")
logger.add(lambda msg: print(msg, end=''), level="TRACE")

json_base_path = "handler/results/"
hosts_base_path = "handler/fetch/hosts/"

def get_commit_id():
    try:
        commit_id = subprocess.check_output(['git', 'rev-parse', 'HEAD'], universal_newlines=True).strip()
        return commit_id
    except subprocess.CalledProcessError:
        print("Failed to get commit id")
        return None

def get_hosts_list():
    return os.listdir(hosts_base_path)

def create_version_file():
    with open('version.txt', 'w') as f:
        f.write(VERSION)

@app.after_request
def log_request(response):
    logger.info(f"{request.method} {request.path} - {response.status_code}")
    return response

@app.route('/')
def index():
    logger.info("Index route called")
    try:
        hosts_files = get_hosts_list()
        commit_id = get_commit_id()
        return render_template('index.j2', hosts_files=hosts_files, commit_id=commit_id, version=VERSION)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return "An error occurred while loading data"

@app.route('/index', methods=['GET', 'POST'])
def details():
    logger.info("Details route called")
    try:
        hosts_files = get_hosts_list()
        commit_id = get_commit_id()
        if request.method == 'GET':
            host_name = request.args.get('host')
            if host_name:
                json_file_path = os.path.join(json_base_path, f"{host_name}.json")
                if os.path.exists(json_file_path):
                    with open(json_file_path) as f:
                        json_content = f.read()
                        logger.debug(f"JSON file content: {json_content}")
                        data = json.loads(json_content)
                    logger.info(f"Data type: {type(data)}")
                    return render_template('index.j2', data=data, host=host_name, hosts_files=hosts_files, version=VERSION, commit_id=commit_id, selected_host=host_name)
                else:
                    return render_template('fallback.j2', hosts_files=hosts_files, version=VERSION, commit_id=commit_id, selected_host=host_name)
            else:
                return "No host selected"
        elif request.method == 'POST':
            # Handle POST requests if needed
            pass
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return render_template('fallback.j2', hosts_files=hosts_files, version=VERSION, commit_id=commit_id, selected_host=host_name)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # handle file upload here
        pass

    return render_template('upload.j2')

@app.route('/update', methods=['POST'])
def update():
    host = request.form.get('host')
    if host:
        results_file = f'handler/results/{host}.json'
        if not os.path.exists(results_file):
            with open(results_file, 'w') as f:
                json.dump({}, f)
        update_service_versions('handler/fetch/hosts/', results_file, 'handler/fetch/id_ed25519')
        return 'OK', 200
    else:
        return 'No host provided', 400

def flask_app():
    create_version_file()
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)
    logger.info("Flask server shutdown.")

if __name__ == '__main__':
    try:
        with logger.catch():
            flask_app()
    except Exception as e:
        logger.error(f"An error occurred: {e}")