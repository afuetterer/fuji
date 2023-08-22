"""
Here we test the Preprocessor class which provides the reference data for a server

Comments to this:
Preprocessor is a singleton, therefore we need to proper tear it up and down.

isDebug=True read the files in fuji_server/data
isDebug=False, run harvesting code

All CI tests should be run with isDebug=True, to not call harvester code
Alternative one would have to mock the server responses to not make real calls.

To test if the harvesting still works there are tests taked with the -noCI and -manual
markers. These tests can be run prior to a release manually.
They mock the fuji_server/data path to not override the files under fuji server

"""
import pytest

from fuji_server.helper.preprocessor import Preprocessor

isDebug = True
fuji_server_dir = './data_test/'

@pytest.fixture()
def temporary_preprocessor() -> Preprocessor:

    # todo: this does not work

    preprocessor = Preprocessor()
    # preprocessor._instance = None
    yield preprocessor

    preprocessor._instance = None


def test_retrieve_licenses(temporary_preprocessor):
    """Test preprocessor if retrieve_licences works"""

    print()
    print('---------------')
    print("licenses")
    print(temporary_preprocessor)
    print(temporary_preprocessor._instance)

    assert temporary_preprocessor.total_licenses == 0
    temporary_preprocessor.retrieve_licenses(isDebug)
    assert temporary_preprocessor.total_licenses > 0
    assert len(temporary_preprocessor.all_licenses) == temporary_preprocessor.total_licenses


# def test_retrieve_datacite_re3repos(temporary_preprocessor):
#     """Test preprocessor if retrieve_re3repos works"""

#     print()
#     print('---------------')
#     print("datacite_re3repos")
#     print(temporary_preprocessor)
#     print(temporary_preprocessor._instance)

#     assert bool(temporary_preprocessor.re3repositories) is False
#     temporary_preprocessor.retrieve_datacite_re3repos()
#     assert bool(temporary_preprocessor.re3repositories) is True
#     assert len(temporary_preprocessor.re3repositories.keys()) > 10




# def test_retrieve_metadata_standards(temporary_preprocessor):
#     """Test preprocessor if retrieve_metadata_standards works"""

#     print()
#     print('---------------')
#     print("metadata_standards")
#     print(temporary_preprocessor)
#     print(temporary_preprocessor._instance)

#     assert bool(temporary_preprocessor.metadata_standards) is False
#     temporary_preprocessor.retrieve_metadata_standards()

#     assert temporary_preprocessor.metadata_standards
#     assert len(temporary_preprocessor.metadata_standards.keys()) > 10


# # todo linked vocab json

# def test_retrieve_linkedvocabs(temporary_preprocessor, test_config):
#     """Test preprocessor if retrieve_linkedvocabs works"""

#     print()
#     print('---------------')
#     print("linked_vocabs")
#     print(temporary_preprocessor)
#     print(temporary_preprocessor._instance)

#     LOV_API = test_config['EXTERNAL']['lov_api']
#     LOD_CLOUDNET = test_config['EXTERNAL']['lod_cloudnet']
#     assert bool(temporary_preprocessor.linked_vocabs) is False
#     # assert not temp_preprocessor.linked_vocabs

#     temporary_preprocessor.retrieve_linkedvocabs(lov_api=LOV_API, lodcloud_api=LOD_CLOUDNET, isDebugMode=isDebug)
#     assert bool(temporary_preprocessor.linked_vocabs) is True
#     assert len(temporary_preprocessor.linked_vocabs) > 10


# def test_preprocessor_rest(temporary_preprocessor):
#     """Test preprocessor if others works"""

#     # METADATACATALOG_API = test_config['EXTERNAL']['metadata_catalog']

#     assert not temporary_preprocessor.default_namespaces

#     temporary_preprocessor.retrieve_default_namespaces()
#     assert len(temporary_preprocessor.default_namespaces) > 10
