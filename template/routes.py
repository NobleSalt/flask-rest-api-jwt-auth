from flask import request,jsonify
from app import app
from .models import Template


@app.route('/template',methods=['POST'])
def create():
    return Template().create()

@app.route('/template',methods=['GET'])
def get_all():
    return Template().fetch_all()

@app.route('/template/<id>',methods=['GET'])
def get_one(id):
    return Template().fetch_one(id)

@app.route('/template/<id>',methods=['UPDATE'])
def update(id):
    return Template().update_one(id=id)

@app.route('/template/<id>',methods=['DELETE'])
def delete(id):
    return Template().delete_one(id=id)
