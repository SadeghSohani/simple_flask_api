from http.client import REQUESTED_RANGE_NOT_SATISFIABLE
import json
import sys
import requests
from time import time
from urllib.parse import urlparse
from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

def connect_db(host, name, user, password):
    db_connection = mysql.connector.connect(
        host = host,
        user = user,
        database = name,
        passwd = password
    )
    mycursor = db_connection.cursor()
    # mycursor.execute("DROP TABLE IF EXISTS devices")
    # mycursor.execute("CREATE TABLE IF NOT EXISTS devices (devIndex INT , devID VARCHAR(255) , name VARCHAR(255), token VARCHAR(255) )")
    mycursor.execute("CREATE TABLE IF NOT EXISTS person (id INT AUTO_INCREMENT PRIMARY KEY, firstName VARCHAR(50) , lastName VARCHAR(50), internationalId VARCHAR(50), typesOfContract VARCHAR(50), eployeeId VARCHAR(50), department VARCHAR(50), address VARCHAR(50), image1 VARCHAR(50), image2 VARCHAR(50), image3 VARCHAR(50) )")
    # mycursor = db_connection.cursor()
    # logging.debug("Database connected:{}".format(db_connection))
    return db_connection

my_db = connect_db("localhost", "mydb", "root", "root@sql*123456789")

@app.route('/person/add', methods = ['POST'])
def add_person() :

    values = request.get_json()
    firstName = values.get('firstName')
    lastName = values.get('lastName')
    internationalId = values.get('internationalId')
    employeeId = values.get('employeeId')
    department = values.get('department')
    typesOfContract = values.get('typesOfContract')
    address = values.get('address')
    image1 = values.get('image1')
    image2 = values.get('image2')
    image3 = values.get('image3')
    
    sql = "INSERT INTO person (firstName, lastName, internationalId, typesOfContract, eployeeId, department, address, image1, image2, image3) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    value = (firstName, lastName, internationalId, employeeId, department, typesOfContract, address, image1, image2, image3)
    mycursor = my_db.cursor()
    mycursor.execute(sql, value)
    my_db.commit()

    response = {
        'message' : 'Person added',
        'body' : values
    }
    return jsonify(response), 200 


if __name__ == '__main__' :
    app.run(host='0.0.0.0', port=sys.argv[1])