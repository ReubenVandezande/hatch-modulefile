from __future__ import annotations

import sys
from pathlib import Path

import pytest

from .utils import build_project, install_project_venv

python_version = ".".join([str(s) for s in sys.version_info[:2]])

@pytest.mark.slow
def test_modulefile(new_project: Path):
    build_project()
    install_directory = install_project_venv()


    modulefile = install_directory.joinpath(
        "lib", f"python{python_version}", "site-packages", "modulefiles", "my-app"
    )
    assert modulefile.exists()

    text = modulefile.read_text()

    requirements = [s.strip() for s in text.split("necessary       {\n")[1].split("}", 1)[0].splitlines()]
    assert requirements == ["my_module"]
    assert get_setting(text, "setenv") == [["QT_XCB_GL_INTEGRATION", "none"]]
    assert get_setting(text, "prepend-path") == [["PATH", "/my/custom/path"]]
    assert get_setting(text, "append-path") == [
        ["OTHER_VARIABLE", "/my/custom/path2"],
    ]


def get_setting(text: str, key: str) -> list[tuple[str, str]]:
    environments = []
    for line in text.splitlines():
        if line.startswith(key):
            environments.append(line.split()[1:])

    return environments
