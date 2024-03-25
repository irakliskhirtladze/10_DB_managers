import json
import pymongo


class DatabaseManager:
    def __init__(self):
        self.client = pymongo.MongoClient("localhost", 27017)
        self.database = self.client["TBC_lecture_10"]

    def create_collection(self, collection_name):
        """Creates a collection in the database"""
        self.database.create_collection(collection_name)

    def check_doc_exists(self, collection_name: str, doc_id):
        """Returns boolean based on whether document with certain ID exist in collection."""
        return self.database[collection_name].count_documents({'_id': doc_id})

    def add_document(self, collection_name: str, doc_id, document: dict):
        """Add a document in collection if it has a unique ID"""
        if not self.check_doc_exists(collection_name, doc_id):
            document = {**{'_id': doc_id}, **document}
            self.database[collection_name].insert_one(document)

    def load_data(self, collection_name: str, projection=None):
        """Loads all data from a collection and returns a generator object.

        Args:
        - collection_name: string
        - projection: optional. To find a specific column, provide dictionary
        where key is a column name and value is boolean or binary (0, 1)"""
        return self.database[collection_name].find({}, projection)

    def delete_document(self, collection_name, doc_id):
        """Deletes a document from specified collection based on ID"""
        self.database[collection_name].delete_one({'_id': doc_id})

    def delete_documents(self, collection_name, doc_ids=None):
        """Deletes many documents from collection if a list of specific IDs is provided.
        Otherwise, deletes all documents"""
        if doc_ids:
            self.database[collection_name].delete_many({'_id': {'$in': doc_ids}})
            return
        self.database[collection_name].delete_many({})

    def get_random_data_ids(self, collection_name: str, sample_size: int):
        """Returns a list of randomly selected non-repeating row IDs of given size"""
        collection = self.database[collection_name]
        total_docs = collection.count_documents({})
        if sample_size > total_docs:
            sample_size = total_docs

        sampled_ids = collection.aggregate([
            {"$sample": {"size": sample_size}},
            {"$project": {"_id": 1}}
        ])

        sampled_id_list = [doc["_id"] for doc in sampled_ids]

        # If the sample size is less than the total number of documents,
        # ensure that the selected document IDs are non-repeating
        if sample_size < total_docs:
            # Calculate the number of additional document IDs needed to reach the sample size
            additional_ids_needed = sample_size - len(sampled_id_list)

            # Select additional document IDs randomly from the collection
            additional_ids = collection.aggregate([
                {"$match": {"_id": {"$nin": sampled_id_list}}},  # Exclude already sampled document IDs
                {"$sample": {"size": additional_ids_needed}},
                {"$project": {"_id": 1}}
            ])

            # Extract the additional document IDs from the cursor
            additional_id_list = [doc["_id"] for doc in additional_ids]

            # Combine the sampled document IDs with the additional document IDs
            sampled_id_list.extend(additional_id_list)

        return sampled_id_list

    def get_relationships(self, collection_1_name: str, collection_2_name: str, id_field_1_name: str,
                          id_field_2_name: str):
        """Retrieve relationships between documents in two collections in a MongoDB database.

        Example: For each advisor (collection_1_name) get all student entries (collection_2_name) this advisor has

        Parameters:
        - collection_1_name: The name of the first collection.
        - collection_2_name: The name of the second collection.
        - id_field_1_name: The name of the field representing the relationship in the first collection.
        - id_field_2_name: The name of the field representing the relationship in the second collection.

        Returns:
        dict: A dictionary where the keys are the relationship values from the first collection
        and the values are lists of documents from the second collection that match the relationship.
        """
        # Query the first collection to retrieve all documents
        collection_1 = self.database[collection_1_name].find()

        # Iterate over documents in the first collection
        relationships = {}
        for doc in collection_1:
            # Get the value of the relationship field from the current document
            relationship_value = doc[id_field_1_name]

            # Query the second collection using the relationship value
            collection_2 = self.database[collection_2_name].find({id_field_2_name: relationship_value})

            # Store the results in the relationships dictionary
            relationships[relationship_value] = list(collection_2)

        return relationships
