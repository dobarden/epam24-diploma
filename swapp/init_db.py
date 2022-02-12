"""
@author: Denis Z
2022
"""

import requests
import json
import pymysql
from datetime import datetime
import variables

conn = pymysql.connect(
    host=variables.host,
    port=variables.port,
    user=variables.user,
    password=variables.password,
    db=variables.database,
)

# Creating tables

cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS planets (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(200) UNIQUE,"
               "gravity VARCHAR(200), climate VARCHAR(200), terrain VARCHAR(200),population BIGINT,url VARCHAR(200),"
               "date VARCHAR(40))")
cursor.execute("CREATE TABLE IF NOT EXISTS characters (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(200) UNIQUE,"
               "gender VARCHAR(20),homeworld VARCHAR(200),height SMALLINT,mass VARCHAR(20),date VARCHAR(40))")


def import_planet():
    """
    Initially adding planet and its residents to the database
    """
    url = "https://swapi.dev/api/planets/1/"
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    response = requests.get(url, headers={'Accept': 'application/json'}, params={format: json})
    data = response.json()
    cur = conn.cursor()
    cur.execute(f"REPLACE INTO planets (name,gravity,climate,terrain,population,url,date) VALUES ('{data['name']}',"
                f"'{data['gravity']}','{data['climate']}','{data['terrain']}','{data['population']}','{data['url']}',"
                f"'{formatted_date}')")
    conn.commit()
    print("----------------")
    print(formatted_date)
    print("Planet: " + data['name'])
    print("----------------")
    print("Residents:")
    for resident in data['residents']:
        resident_url = resident
        resident_response = requests.get(resident_url, headers={'Accept': 'application/json'}, params={format: json})
        resident_data = resident_response.json()
        print(resident_data['name'])
        cur = conn.cursor()
        cur.execute(f"REPLACE INTO characters (name,gender,homeworld,height,mass,date) "
                    f"VALUES ('{resident_data['name']}','{resident_data['gender']}','{resident_data['homeworld']}',"
                    f"'{resident_data['height']}','{resident_data['mass']}','{formatted_date}')")
        conn.commit()
    print("----------------")


import_planet()
conn.close()
