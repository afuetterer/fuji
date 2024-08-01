# SPDX-FileCopyrightText: 2020 PANGAEA (https://www.pangaea.de/)
#
# SPDX-License-Identifier: MIT

from pathlib import Path

from dynaconf import Dynaconf

ROOT_DIR = Path(__file__).parent

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    root_path="fuji_server/config",
    settings_files=["settings.toml"],
)

settings.service.metric_yml_path = ROOT_DIR / settings.service.yaml_directory

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
