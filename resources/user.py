from flask_restful import Resource, reqparse
from flask import jsonify, make_response
import pymysql

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('gender')
parser.add_argument('birth')
parser.add_argument('note')
class Users(Resource):
    def db_init(self):
        db = pymysql.connect('192.168.56.106','joyce','Pn123456','API_server_database')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor
    def get(self):
        db = pymysql.connect('192.168.56.106','joyce','Pn123456','API_server_database')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        sql = """Select * From API_server_database.users where deleted = False"""
        cursor.execute(sql)
        users = cursor.fetchall()
        db.close()
        response = {
            'data':users
        }
        return make_response(jsonify(response), 201)
    
    def post(self):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        if arg['birth'] == None:
            return make_response(jsonify({'msg':'未填寫生日'}), 400)
        user = {
            'name':arg['name'],
            'gender':arg['gender'],
            'birth':arg['birth'] or '1900-01-01',
            'note':arg['note'],
        }
        sql = """
            Insert into API_server_database.users
            (name, gender, birth, note )
            values('{}','{}','{}','{}')
        """.format(user['name'],user['gender'],user['birth'],user['note'])
        cursor.execute(sql)
        db.commit()
        db.close()
        response = {
            'result':True
        }
        return jsonify(response)

class User(Resource):
    def db_init(self):
        db = pymysql.connect('192.168.56.106','joyce','Pn123456','API_server_database')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor
    def get(self, id):
        db, cursor = self.db_init()
        sql = """Select * From API_server_database.users 
                where id = '{}'
        """.format(id)
        cursor.execute(sql)
        user = cursor.fetchall()
        db.close()
        response = {
            'data':user
        }
        return jsonify(response)

    def patch(self, id):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        user = {
            'name':arg['name'],
            'gender':arg['gender'],
            'birth':arg['birth'] or '1900-01-01',
            'note':arg['note'],
        }
        query = []
        for key, value in user.items():
            if value != None:
                query.append(key + ' = '+ "'{}'".format(value))
        query = ','.join(query)
        sql = """
            Update API_server_database.users Set{} where id = "{}"
        """.format(query, id)
        cursor.execute(sql)
        db.commit()
        db.close()
        response = {
            'result':True
        }
        return jsonify(response)

    def delete(self, id):
        db, cursor = self.db_init()
        sql = """Update API_server_database.users Set deleted = True
                where id = '{}'
        """.format(id)
        cursor.execute(sql)
        cursor.fetchall()
        db.commit()
        db.close()
        response = {
            'result':True
        }
        return jsonify(response)


