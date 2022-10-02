import os
from importlib.machinery import SourceFileLoader
from pathlib import Path

from pkg_resources import parse_requirements
from setuptools import setup, find_packages


MODULE_NAME = "simple_server"
BASE_DIR = Path(__file__).parent.resolve()

module = SourceFileLoader("main", os.path.join("main/__init__.py")).load_module("main")


def load_requirements(fname: str) -> list:
    requirements = []
    with open(fname, "r") as fp:
        for req in parse_requirements(fp.read()):
            extras = "[{}]".format(",".join(req.extras)) if req.extras else ""
            requirements.append(f"{req.name}{extras}{req.specifier}")
    return requirements


setup(
    name=MODULE_NAME,
    version=module.__version__,
    author=module.__author__,
    description=module.__doc__,
    long_description=open(BASE_DIR / "README.md").read(),
    url="https://github.com/Neznakomec16/simple_server",
    platforms="all",
    classifiers=["Operating System :: POSIX", "Programming Language :: Python :: 3.10",],
    python_requires=">=3.9.0",
    packages=find_packages(),
    install_requires=load_requirements("requirements/requirements-base.txt"),
    entry_points={
        "console_scripts": [
            f"{MODULE_NAME}-app = {MODULE_NAME}.app.__main__:main",
            f"{MODULE_NAME}-db = {MODULE_NAME}.db.__main__:main",  # todo: Imlement db
        ]
    },
    include_package_data=True,
)
