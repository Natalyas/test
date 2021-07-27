# coding=utf-8
import json
from elasticsearch import Elasticsearch, RequestsHttpConnection,Urllib3HttpConnection
from bson import json_util
from bson.objectid import ObjectId

class TaskDAO(Elasticsearch):

    def __init__(self,database):
        self.database = database

    def create(self, data):
        task = {
            'title': data.get('title'),
            'description': data.get('description'),
            'done': False
        }
        query = {
            'query': {
                "bool": {
                    "must" : {
                        "match" : { 'done': False },
                        "match" : { 'title': data.get('title') },
                        "match" : { 'description': data.get('description') }
                    }
                }
            }
        }

        task = self.database.search(index="test-index", body=query)
        return self.to_json(task)

    def list(self):
        query = {
            'size' : 10000,
            'query': {
                'match_all' : {}
            }
        }
        tasks = self.database.search(index="test-index", body=query)
        return self.to_json(tasks)

    def read(self, object_id):
        query = {
            "query": {
                "ids" : {
                    "values" : [ ObjectId(object_id) ]
                }
            }
        }
        print(self.database.search(index="test-index", body=query))
        task = self.database.search(index="test-index", body=query)
        return self.to_json(task)

    def update(self):
        pass

    def delete(self):
        pass

    def to_json(self, data):
        return json.loads(json_util.dumps(data))
