"""Base class for collections

Used as base for Vehicles, Devices etc collections and
provides a common interface for all collections.
"""

class Collection:
    """Base class for collections
    """

    def __init__(self, cname, db):
        """Initialise

        cname -- collection name
        db    -- firestore database client
        """
        self.cname = cname
        self.db = db

        # ---- collection reference
        self.coll_ref = self.db.collection(self.cname)

    def get(self, key, value, limit=None):
        """Get document(s) from collection

        Get documents from the collection whose field (key)
        matches the supplied value.

        return -- documents that match
        key    -- field to filter on
        value  -- value to filter on
        """

        docs = self.coll_ref.where(key, "==", value)

        if limit:
            docs = docs.limit(limit)

        return docs.get()

    def getone(self, key, value):
        """Get first matching document

        Typically used when expecting only one document (ie key
        represents a unique value).

        Queries return a generator, need to extract the first document
        from the generator (next()).
        """
        docs = self.get(key, value, limit=1)

        # ---- get first document, None if no documents
        doc = next(docs, None)

        # ---- convert document to dictionary
        coll_id = ""
        doc_dict = None
        if doc:
            doc_dict = doc.to_dict()
            coll_id = doc.id

        return coll_id, doc_dict

    def new(self, doc):
        """Create a new document

        return -- document reference for the new document
        doc  -- document (dict) to create
        """

        # ---- create document reference
        ref = self.coll_ref.document()

        self.coll_ref.document(ref.id).set(doc, merge=False)

        return ref.id
