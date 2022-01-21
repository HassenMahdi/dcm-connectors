from connectors.connector import Connector
from pymongo import MongoClient

class MongoDBConnector(Connector):

    def __init__(self, host=None, user=None, password=None, port=None, database=None,  **kwargs):
        self.host = host
        self.port = port
        self.db = database
        self.user = user
        self.password = password

    def get_client(self):
        =mongodb://berexia:Berexia934jY@13.36.203.148:27017/ghpsj?retryWrites=false&authSource=admin
        if self.user and self.password:
            mongo_uri = f"mongodb://{self.user}:{self.password}@{self.database}:{self.port}/{self.database}?retryWrites=false&authSource=admin"
        else:
            mongo_uri = f"mongodb://{self.database}:{self.port}/{self.database}?retryWrites=false"

        return MongoClient(mongo_uri)

    def upload_df(self, df, collection=None,insertion_script=None,**kwargs):
        client = self.get_client()
        col = client[self.db][collection]

        if insertion_script:
            exec(insertion_script)
        else:
            for row in df.to_dict(orient='records'):
                _id = row.get("_id", generate_id())
                del row["_id"]
                col.update_one({"_id": _id}, {"$set": row}, upsert=True)


    def get_df(self, collection=None, query=None ,**kwargs):
        db = self.get_client()[self.db]
        col = db[collection]

        evaled_query = []
        if query:
            evaled_query = eval(query)

        result = col.aggregate(evaled_query)

        df = pd.DataFrame([flatten(d) for d in result])
        return df