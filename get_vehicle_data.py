"""Get vehicle data

Given a Vehicle Registration Mark (VRM), obtains vehicle
details from an external service (eg Cazana - http://cazana.com).
The vehicle data is cached in a vehicles collection which is updated
whenever the data in the cache expires (see CFG.VEHICLE_DATA_EXPIRY
which defines the expiry in days).
"""

import time
from google.cloud import firestore
from utils import get_days, remspace
from config import CFG
from vehicles_collection import VehiclesCollection

def get_vehicle_data(db, vrm):
    """Get vehicle data for given VRM

    return -- dictionary containing vehicle data, None if vehicle not found
    db     -- firestore client
    vrm    -- Vehicle Registration Mark (eg "AA99 AAA")
    """

    try:
        # ---- create object for access to cloud firestore
        vcoll = VehiclesCollection(db)

        # ---- get vehicle data from cloud firestore
        coll_id, vehicle = vcoll.getone(vrm=vrm)

        if not vehicle:
            # ---- vehicle does not exist
            #      create new vehicle document. Setting updateRequired
            #      triggers another process to update this document with
            #      the vehicle details

            vehicle = {"vrm": vrm, "updateRequired": True}
            coll_id = vcoll.new(vehicle)

        else:
            # ---- check if vehicle document has expired
            today = get_days()
            last_update = get_days(vehicle.get("last_update", 0))
            expired = (today - last_update) > CFG.VEHICLE_DATA_EXPIRY

            if expired:
                # ---- set updateRequired flag
                #      thisc will trigger an update of the document

                vehicle["updateRequired"] = True
                vehicle["last_update"] = int(time.time())
                vcoll.save(coll_id, vehicle, merge=True)

    except Exception as exc:
        # ---- TBA handle expected exceptions
        raise

    return vehicle

if __name__ == "__main__":
    import sys


    def main():
        """Standalone script for testing
        """

        # ---- create Firestore client
        db = firestore.Client()

        if len(sys.argv) > 1:
            vrm = sys.argv[1]
        else:
            # ---- use default value
            vrm = "AA11FRD"

        vehicle = get_vehicle_data(db, vrm)
        print("vehicle: {}".format(vehicle))

    main()
