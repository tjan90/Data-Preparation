from flask import Flask, request
from flask_restful import Resource, Api
import csv
import json

app = Flask(__name__)
api = Api(app)

position = 0
class Titanic_Survivors(Resource):
    def __init__(self, filename):
        with open(filename, 'r') as f:
            self.data_list = [x.strip() for x in f.readlines()]

    def get(self):
        try:
            global position
            position += 1
            return {"data": f'{self.data_list[position]}'}
        except Exception as e:
            return {"error": f"{e}"}

api.add_resource(Titanic_Survivors, 
                 '/survivors',
                 resource_class_kwargs={'filename': 'titanic_dataset/train.csv'})


if __name__ == '__main__':
    app.run()

