[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
# Simple auth server
***
Simple template server based on FastAPI framework

The key features:
+ [aiohttp](https://docs.aiohttp.org/en/v3.7.4/web_advanced.html#aiohttp-web-signals)-like signals to configure all services at startup

## Installation
```shell
pip install -r requirements/requirements-base.txt
pip install -e .
```
 OR
 
```shell
docker build --tag simple_server .
docker run -p 8080:8080 -d simple_server
```


## Run

```
usage: simple_server-app [-h] [--host HOST] [--port PORT] [--env_file ENV_FILE]

options:
  -h, --help           show this help message and exit
  --host HOST
  --port PORT
  --env_file ENV_FILE
```


Required variables described at [.env_example](./.env_example)