"""Class to interface to vehicles collection
"""


from google.cloud import firestore
from collection import Collection

class VehiclesCollection(Collection):
    """Interface to Vehicles collection

    Provides a set of methods specific to manipulating the vehicles
    collection in firestore.
    """

    # ---- collection name
    cname = "vehicles"

    def __init__(self, db):
      """Initialise vehicles collection

      db  -- firestore database client
      """
      super(VehiclesCollection, self).__init__(VehiclesCollection.cname, db)

    def getone(self, vrm):
        """Return single matching vehicle

        return -- document id, vehicle document (dict)
        vrm    -- Vehicle Registration Mark
        """
        return super(VehiclesCollection, self).getone("data.vrm", vrm)

    def save(self, doc_id, vehicle, merge=True):
        """Save document

        If merge=True, merge the document into an existing document, otherwise
        overwrite it.

        doc_id  -- document id
        vehicle -- vehicle document (dict)
        merge   -- boolean
        """

        super(VehiclesCollection, self).save(doc_id, vehicle, merge=merge)


if __name__ == "__main__":
    def main():
        db = firestore.Client()
        vehicles = VehiclesCollection(db)

        vrm = "AA99FRD"
        id, vehicle = vehicles.getone(vrm=vrm)

        print("id: {}, vrm: {}, vehicle: {}".format(id, vrm, vehicle))

    main()
