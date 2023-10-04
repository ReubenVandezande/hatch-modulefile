import subprocess
import sys
from pathlib import Path


def build_project(*args):
    if not args:
        args = ["-w"]

    command = [sys.executable, "-m", "build", *args]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True)  # noqa: S603



def install_project():
    wheel = next(iter(Path.cwd().glob("dist/*.whl")))
    userbase = Path.cwd().joinpath("build")
    userbase.mkdir()
    command = f"{sys.executable} -m pip install {str(wheel)} -t build"
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True, shell=True)  # noqa: S603, S602
