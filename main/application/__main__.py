import argparse
from pathlib import Path

import uvicorn

from main.application.app import create_app
from main.application.config import Config


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="localhost")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--env_file", type=Path, default=None)
    args = parser.parse_args()

    config = Config.get_from_env() if args.env_file is None else Config.get_from_env_file(args.env_file)
    app = create_app(config)
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    cli()
