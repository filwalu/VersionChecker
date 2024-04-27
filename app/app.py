from flask import Flask, request, render_template
from loguru import logger
import json
import os


app = Flask(__name__)

logger.add("app.log", rotation="10 MB", retention="7 days", level="DEBUG")
logger.add(lambda msg: print(msg, end=''), level="TRACE")

json_base_path = "handler/results/"
hosts_base_path = "handler/ansible/hosts/"

@app.after_request
def log_request(response):
    logger.info(f"{request.method} {request.path} - {response.status_code}")
    return response

@app.route('/')
def index():
    logger.info("Index route called")
    try:
        hosts_files = os.listdir(hosts_base_path)
        host_name = request.args.get('host')
        if host_name:
            json_file_path = os.path.join(json_base_path, f"{host_name}.json")
            if os.path.exists(json_file_path):
                with open(json_file_path) as f:
                    json_content = f.read()
                    logger.debug(f"JSON file content: {json_content}")
                    data = json.loads(json_content)
                logger.info(f"Data type: {type(data)}")
                return render_template('index.j2', data=data, host=host_name, hosts_files=hosts_files)
            else:
                return "No info about host"
        else:
            return render_template('hosts.j2', hosts_files=hosts_files)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return "An error occurred while loading data"

def flask_app():
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)
    logger.info("Flask server shutdown.")

if __name__ == '__main__':
    try:
        with logger.catch():
            flask_app()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
