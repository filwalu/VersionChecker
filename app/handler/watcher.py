import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json
import os
from loguru import logger

class Watcher:
    DIRECTORY_TO_WATCH = "handler/fetch/hosts/"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()


class Handler(FileSystemEventHandler):
    @staticmethod
    def process(event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.src_path
            path to the changed file
        """
        logger.info(f"Processing event: {event.event_type} - {event.src_path}")
        # Take any action here when a file is first created or modified
        if event.event_type in ['created', 'modified']:
            if os.path.isfile(event.src_path):
                Handler.create_results_file(event.src_path)

    @staticmethod
    def create_results_file(host_file):
        try:
            logger.info(f"Creating results file for host file: {host_file}")
            base_name = os.path.basename(host_file)
            host_name, _ = os.path.splitext(base_name)
            results_file = f'handler/results/{host_name}.json'
            if not os.path.exists(results_file):
                logger.info(f"Results file for {host_name} does not exist. Creating it.")
                with open(host_file, 'r') as f:
                    data = json.load(f)
                    services = [service.strip() for service in data['services'].split(',')]
                    results = {service: "null" for service in services}
                with open(results_file, 'w') as f:
                    json.dump(results, f, indent=4)
                logger.info(f"Results file for {host_name} created successfully.")
            else:
                logger.info(f"Results file for {host_name} already exists. Skipping creation.")
        except Exception as e:
            logger.error(f"Failed to create results file for {host_file}: {e}")

    def on_created(self, event):
        self.process(event)

    def on_modified(self, event):
        self.process(event)
