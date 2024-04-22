# VersionChecker
project_name/
│
├── app/
│   ├── frontend/
│   │   ├── static/
│   │   │   ├── css/
│   │   │   │   └── style.css
│   │   │   └── js/
│   │   │       └── script.js
│   │   └── templates/
│   │       ├── index.html
│   │       └── results.html
│   ├── handler/
│   │   ├── __init__.py
│   │   ├── playbook_handler.py
│   │   └── result_handler.py
│   ├── playbook/
│   │   ├── playbook1.yml
│   │   └── playbook2.yml
│   ├── app.py
│   └── requirements.txt
│
└── docker/
    ├── docker-compose.yml
    └── Dockerfile
[\[git clone \](https://github.com/filwalu/VersionChecker.git)](https://github.com/filwalu/VersionChecker.git)
cd docker
docker build -t VersionChecker .