"""
Configurations and fixtures for fuji_server tests
"""
import configparser
import pickle
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from fuji_server.app.fuji_app import create_fuji_app
from fuji_server.helper.preprocessor import Preprocessor

if TYPE_CHECKING:
    from flask.app import Flask
    from flask.testing import FlaskClient

ROOT_DIR = Path(__file__).parent.parent
SRC_DIR = ROOT_DIR.joinpath("fuji_server")
TESTS_PATH = ROOT_DIR.joinpath("tests")
TEST_CONFIG_FILE_PATH = TESTS_PATH.joinpath("config", "test_server.ini")

@pytest.fixture(scope="session")
def test_config():
    """Fixture returning the read config object by configparser"""
    config = configparser.ConfigParser()
    config.read(TEST_CONFIG_FILE_PATH)
    return config

@pytest.fixture(scope="session")
def preprocessor(test_config) -> Preprocessor:

    YAML_DIR = test_config["SERVICE"]["yaml_directory"]
    METRIC_YML_PATH = SRC_DIR.joinpath(YAML_DIR)
    LOV_API = test_config["EXTERNAL"]["lov_api"]
    LOD_CLOUDNET = test_config["EXTERNAL"]["lod_cloudnet"]

    preprocessor = Preprocessor()

    print()
    print('---------------')
    print("preprocessor")
    print(preprocessor)
    print(preprocessor._instance)


    preprocessor.set_metric_yaml_path(METRIC_YML_PATH)
    isDebug = True
    preprocessor.retrieve_licenses(isDebug)
    preprocessor.retrieve_datacite_re3repos()
    preprocessor.retrieve_metadata_standards()
    preprocessor.retrieve_linkedvocabs(lov_api=LOV_API, lodcloud_api=LOD_CLOUDNET, isDebugMode=isDebug)
    preprocessor.retrieve_default_namespaces()
    preprocessor.set_remote_log_info(
        test_config["SERVICE"]["remote_log_host"], test_config["SERVICE"]["remote_log_path"]
    )

    return preprocessor


    # initialize_preprocessor(test_config)
    # return Preprocessor

@pytest.fixture(scope="session")
def app(test_config, preprocessor: Preprocessor) -> "Flask":
    _app = create_fuji_app(test_config)
    _app.testing = True
    return _app.app






@pytest.fixture(scope="session")
def client(app: "Flask") -> "FlaskClient":
    """A flask test_client."""
    with app.test_client() as test_client:
        yield test_client






#TODO: fixture?
# autouse?

# def initialize_preprocessor(test_config):
#     print()
#     print('------------------------')
#     print(test_config)

#     """Function which populates the preprocessor from __main__"""

#     YAML_DIR = test_config["SERVICE"]["yaml_directory"]
#     METRIC_YML_PATH = SRC_DIR.joinpath(YAML_DIR)
#     LOV_API = test_config["EXTERNAL"]["lov_api"]
#     LOD_CLOUDNET = test_config["EXTERNAL"]["lod_cloudnet"]

#     preprocessor = Preprocessor()
#     preprocessor.set_metric_yaml_path(METRIC_YML_PATH)
#     isDebug = True
#     preprocessor.retrieve_licenses(isDebug)
#     preprocessor.retrieve_datacite_re3repos()
#     preprocessor.retrieve_metadata_standards()
#     preprocessor.retrieve_linkedvocabs(lov_api=LOV_API, lodcloud_api=LOD_CLOUDNET, isDebugMode=isDebug)
#     preprocessor.retrieve_default_namespaces()
#     preprocessor.set_remote_log_info(
#         test_config["SERVICE"]["remote_log_host"], test_config["SERVICE"]["remote_log_path"]
#     )


# @pytest.fixture
# def temp_preprocessor():
#     """Fixture which resets the Preprocessor (singleton) for a test and restores its prior state afterwards"""
#     preprocessor = Preprocessor

#     DUMP_PATH = Path("temp_proprocessor_dump.pkl")
#     # save current state
#     with open(DUMP_PATH, "bw") as fileo:
#         pickle.dump(preprocessor, fileo)

#     # resetting the preprocessor (everything from class header)
#     preprocessor.all_metrics_list = []
#     preprocessor.formatted_specification = {}
#     preprocessor.total_metrics = 0
#     preprocessor.total_licenses = 0
#     preprocessor.METRIC_YML_PATH = None
#     preprocessor.SPDX_URL = None
#     preprocessor.DATACITE_API_REPO = None
#     preprocessor.RE3DATA_API = None
#     preprocessor.LOV_API = None
#     preprocessor.LOD_CLOUDNET = None
#     preprocessor.BIOPORTAL_API = None
#     preprocessor.BIOPORTAL_KEY = None
#     preprocessor.schema_org_context = []
#     preprocessor.all_licenses = []
#     preprocessor.license_names = []
#     preprocessor.metadata_standards = {}  # key=subject,value =[standards name]
#     preprocessor.metadata_standards_uris = {}  # some additional namespace uris and all uris from above as key
#     preprocessor.science_file_formats = {}
#     preprocessor.long_term_file_formats = {}
#     preprocessor.open_file_formats = {}
#     preprocessor.re3repositories = {}
#     preprocessor.linked_vocabs = {}
#     preprocessor.default_namespaces = []
#     preprocessor.standard_protocols = {}
#     preprocessor.resource_types = []
#     preprocessor.identifiers_org_data = {}
#     preprocessor.google_data_dois = []
#     preprocessor.google_data_urls = []
#     # preproc.fuji_server_dir = os.path.dirname(os.path.dirname(__file__))  # project_root
#     preprocessor.header = {"Accept": "application/json"}
#     # preproc.logger = logging.getLogger(__name__)
#     preprocessor.data_files_limit = 3
#     preprocessor.metric_specification = None
#     preprocessor.remote_log_host = None
#     preprocessor.remote_log_path = None

#     yield preprocessor

#     # tear down code, restore the state
#     with open(DUMP_PATH, "br") as fileo:
#         preprocessor = pickle.load(fileo)
#     DUMP_PATH.unlink()
