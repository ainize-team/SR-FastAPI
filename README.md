# SR-FastAPI

[![Github Contributors](https://img.shields.io/github/contributors/ainize-team/SR-FastAPI)](https://github.com/badges/ainize-team/SR-FastAPI/contributors)
[![GitHub issues](https://img.shields.io/github/issues/ainize-team/SR-FastAPI.svg)](https://github.com/ainize-team/SR-FastAPI/issues)
![Github Last Commit](https://img.shields.io/github/last-commit/ainize-team/SR-FastAPI)
![Github Repository Size](https://img.shields.io/github/repo-size/ainize-team/SR-FastAPI)
[![GitHub Stars](https://img.shields.io/github/stars/ainize-team/SR-FastAPI.svg)](https://github.com/ainize-team/SR-FastAPI/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/ainize-team/SR-FastAPI.svg)](https://github.com/ainize-team/SR-FastAPI/network/members)
[![GitHub Watch](https://img.shields.io/github/watchers/ainize-team/SR-FastAPI.svg)](https://github.com/ainize-team/SR-FastAPI/watchers)

![Supported Python versions](https://img.shields.io/badge/python-3.8-brightgreen)
[![Imports](https://img.shields.io/badge/imports-isort-brightgreen)](https://pycqa.github.io/isort/)
[![Code style](https://img.shields.io/badge/code%20style-black-black)](https://black.readthedocs.io/en/stable/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://pre-commit.com/)
![Package Management](https://img.shields.io/badge/package%20management-poetry-blue)

## Description

FastAPI Server for Super Resolution Model.

## Installation

```
docker build -t sr-fastapi .
```

## Usage

```
docker run -d --name <server_container_name> -p 8000:8000 \
-e APP_NAME=<server_app_name> \
-e BROKER_URI=<broker_uri> \
-e FIREBASE_APP_NAME=<firebase_app_name> \
-e DATABASE_URL=<firebase_realtime_database_url> \
-e STORAGE_BUCKET=<firebase_storage_url> \
-v <firebase_credential_path>:/app/key \
sr-fastapi
```

## License

[![Licence](https://img.shields.io/github/license/ainize-team/SR-FastAPI.svg)](./LICENSE)
