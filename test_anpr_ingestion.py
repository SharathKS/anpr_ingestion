"""anpr_ingestion tests

Need to install pytest to run these tests:
    pip install pytest

To run the tests in this file:
    pytest -v --capture=no test_anpr_ingestion.py 

The flag "--capture=no" will display any output to stdout otherwise
it will not be seen.

By convention, tests that are supposed to be successful have the "_ok"
suffix and tests that verify a failure condition have the suffix "_fail".
"""

from google.cloud import firestore
from vehicles_collection import VehiclesCollection

def test_vrm_does_not_exist_fail():
    """Verify invalid VRM not found in data store
    """

    # ---- create Firestore client
    db = firestore.Client()

    # ---- create object to interface to vehicles collections
    vcoll = VehiclesCollection(db)

    # ---- attempt to retrieve with invalid VRM
    vrm = "invalid-invalid"

    doc_id, vehicle = vcoll.getone(vrm=vrm)

    assert doc_id == ""
    assert vehicle is None


def test_vrm_exists_ok():
    """Verify valid VRM that exists returns expected data

    Create an entry for a VRM and then verify that it can be
    read back and contains the expected data. For the purposes
    of this test, use the text "TEST" in the VRM to make it
    easy to remove the test entries.

    TBA: if the document exists already, new() will create another
    (same vrm, different doc_id). When retrieving the vehicle using
    getone() there is no guarantee that the one you just created will
    be the one returned.
    """

    # ---- create Firestore client
    db = firestore.Client()

    # ---- create object to interface to vehicles collections
    vcoll = VehiclesCollection(db)

    # ---- create vehicle document
    vrm = "AA01 TEST"
    vehicle = {"vrm": vrm, "colour": "red"}
    doc_id = vcoll.new(vehicle)

    # ---- retrieve vehicle document
    doc_id2, vehicle2 = vcoll.getone(vrm=vrm)

    assert doc_id == doc_id2
