from __future__ import annotations

import logging
import os
import tempfile
from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

from hatch_modulefile.inputs import ModulefileInputs


class ModulefileBuildHook(BuildHookInterface):
    PLUGIN_NAME = "modulefile"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__modulefile_path = None
        self.__inputs = None

    @property
    def inputs(self) -> ModulefileInputs:
        if self.__inputs is None:
            self.__inputs = ModulefileInputs(self.config, Path.cwd())

        return self.__inputs

    def initialize(self, version: str, build_data: dict[str, str]):
        if self.target_name != "wheel":
            return

        project_name = self.build_config.builder.metadata.core.name
        modulefile_path = self.generate_modulefile()
        file_name = f"modulefiles/{project_name}"
        # Would like this eventually!
        # build_data['extra_metadata']['shared-data'] = [{str(modulefile_path): "modulefiles/module"}]

        if version == "editable":  # no cov
            build_data["force_include_editable"][str(modulefile_path)] = file_name
        else:
            build_data["force_include"][str(modulefile_path)] = file_name

        if self.inputs.site_customize:
            self.generate_site_customize(version, build_data)

    def generate_site_customize(self, version: str, build_data: dict[str,str]):
        # Add sitecustomize file to force multiple site-packages to load
        site_customize_path = Path(__file__).parent.joinpath("_sitecustomize.py")
        if version == "editable":  # no cov
            build_data["force_include_editable"][str(site_customize_path)] = "sitecustomize.py"
        else:
            build_data["force_include"][str(site_customize_path)] = "sitecustomize.py"

    def generate_modulefile(self) -> Path:
        """Generate a modulefile from pyproject.toml inputs

        Returns
        -------
        Path
            Path to temporary modulefile
        """
        modulefile_path = self.inputs.modulefile_path
        if self.inputs.modulefile_path is not None:
            modulefile_path = self.inputs.modulefile_path
            if not modulefile_path.exists():
                msg = f"Cannot find specified modulefile: {modulefile_path}"
                raise ValueError(msg)
        else:
            file_descriptor, modulefile_path = tempfile.mkstemp()
            self.__modulefile_path = modulefile_path
            with open(file_descriptor, "w") as file_handle:
                file_handle.write(self.inputs.generate_modulefile_string())

        return Path(modulefile_path)

    def finalize(self, version, build_data, artifact_path):  # noqa: ARG002
        try:
            if self.__modulefile_path is not None:
                os.remove(self.__modulefile_path)
        except Exception:
            msg = f"Failed to delete existing tmp file: {self.__modulefile_path}"
            logging.getLogger(__name__).warning(msg)
            pass
