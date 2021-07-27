# coding=utf-8
from flask import Flask, jsonify, request, abort
from task import TaskDAO
from elasticsearch import Elasticsearch


app = Flask('todoapp')
mapping = {
    "mappings" : {
        "properties": {
            'done': { "type":  "boolean" },
            'title': { "type":  "text" },
            'description': { "type":  "text" }
         }
    }
}

client = Elasticsearch(["es-test:9200"])
client.indices.create(index="test-index",body=mapping, ignore=400)
tasks_dao = TaskDAO(client)

@app.route('/tasks')
def list():
    return jsonify(tasks_dao.list()), 200


@app.route('/tasks/<pk>', methods=['GET', 'PUT'])
def get(pk):
    if request.method == 'GET':
        return jsonify(tasks_dao.read(pk))


@app.route('/tasks', methods=['POST'])
def create():
    if request.method == 'POST':
        data = request.json
        title = data.get('title', None)
        description = data.get('description', None)

        if not title or not description:
            return "The fields 'title' and 'description' are required", 400

        task = tasks_dao.create(data)

        return jsonify(task), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0")
