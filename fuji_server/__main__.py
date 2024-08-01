#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2020 PANGAEA (https://www.pangaea.de/)
#
# SPDX-License-Identifier: MIT

import argparse
import configparser
import logging
import logging.config
from pathlib import Path

from dynaconf import Dynaconf
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from fuji_server.app import create_app
from fuji_server.helper.preprocessor import Preprocessor

ROOT_DIR = Path(__file__).parent


def main(settings):
    METRIC_YML_PATH = ROOT_DIR / settings.service.yaml_directory
    logger.info("YAML PATH: %s", METRIC_YML_PATH)

    LOV_API = settings.external.lov_api
    LOD_CLOUDNET = settings.external.lod_cloudnet

    DEBUG = settings.service.debug_mode
    DATA_FILES_LIMIT = settings.service.data_files_limit
    MAX_CONTENT_SIZE = settings.service.max_content_size
    REMOTE_LOG_HOST = settings.service.remote_log_host
    REMOTE_LOG_PATH = settings.service.remote_log_path
    RATE_LIMIT = settings.service.rate_limit
    SERVICE_HOST = settings.service.service_host
    SERVICE_PORT = settings.service.service_port

    preproc = Preprocessor()

    preproc.set_data_files_limit(DATA_FILES_LIMIT)
    preproc.set_metric_yaml_path(METRIC_YML_PATH)
    preproc.set_max_content_size(MAX_CONTENT_SIZE)
    preproc.set_remote_log_info(REMOTE_LOG_HOST, REMOTE_LOG_PATH)

    preproc.retrieve_licenses(DEBUG)
    preproc.retrieve_datacite_re3repos()
    preproc.retrieve_metadata_standards()
    preproc.retrieve_linkedvocabs(lov_api=LOV_API, lodcloud_api=LOD_CLOUDNET, isDebugMode=DEBUG)

    logger.info("Total SPDX licenses: %s", preproc.get_total_licenses())
    logger.info("Total re3repositories found from datacite api: %s", len(preproc.getRE3repositories()))
    logger.info("Total subjects area of imported metadata standards: %s", len(preproc.metadata_standards))
    logger.info("Total LD vocabs imported: %s", len(preproc.getLinkedVocabs()))
    logger.info("Total default namespaces specified: %s", len(preproc.getDefaultNamespaces()))

    print(settings.service)

    app = create_app(settings)

    Limiter(get_remote_address, app=app.app, default_limits=[RATE_LIMIT])
    # built in uvicorn ASGI
    app.run(host=SERVICE_HOST, port=SERVICE_PORT)


def configure_logger(settings):
    log_configfile = ROOT_DIR / settings.service.log_config
    log_directory = ROOT_DIR / settings.service.logdir
    log_file_path = log_directory / "fuji.log"
    if not log_directory.exists():
        log_directory.mkdir(exist_ok=True)

    logging_config = configparser.ConfigParser()
    logging_config.read(log_configfile)
    logging.config.fileConfig(log_configfile, defaults={"logfilename": log_file_path})
    logger = logging.getLogger(__name__)

    # TODO: this does not work
    logging.getLogger("connexion").setLevel("INFO")
    return logger


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", required=True, help="Path to server.ini config file")
    args = parser.parse_args()
    config_path = args.config

    # load application config
    settings = Dynaconf(settings_file=config_path)
    print(settings)

    # load logging config
    logger = configure_logger(settings)

    main(settings)
