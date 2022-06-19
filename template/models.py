from passlib.hash import pbkdf2_sha256
from app import db
import uuid
from flask import Flask, jsonify, request


class Template:

    def create(self):
        temp = {
            "_id": uuid.uuid4().hex,
            "template_name": request.get_json().get("template_name"),
            "subject": request.get_json().get("subject"),
            "body": request.get_json().get("body"),
        }

        if db.template.insert_one(temp):
            return jsonify({"message": "Successfully Added New Template"}), 200

        return jsonify({"error": "There is an problem with your data !"}), 400

    def fetch_one(self, id):
        single_temp = db.template.find_one({"_id": id})
        if single_temp:
            return jsonify(single_temp), 200

        return jsonify({"error": "This template was not found !"}), 400

    def delete_one(self, id):
        single_temp = db.template.find_one({"_id": id})
        if single_temp:
            db.template.delete_one({"_id": id})
            return jsonify({"message": "You Have Successfully Deleted A Template"}), 200

        return jsonify({"error": "This template was not found !"}), 400

    def fetch_all(self):
        all_data = db.template.find({})

        return jsonify(list(all_data)), 200

    def update_one(self, id, update):
        single_temp = db.template.find_one({"_id": id})
        if single_temp:

            return jsonify(single_temp), 200

        return jsonify({"error": "This template was not found !"}), 400
