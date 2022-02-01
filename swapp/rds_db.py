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

def import_planet(name):
    """
    Initially adding planet and its residents to the database
    """
    url = name
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    response = requests.get(url, headers={'Accept':'application/json'}, params={format:json})
    data = response.json()
    cur = conn.cursor()
    cur.execute(f"REPLACE INTO planets (name,gravity,climate,terrain,population,url,date) VALUES ('{data['name']}','{data['gravity']}','{data['climate']}','{data['terrain']}','{data['population']}','{data['url']}','{formatted_date}')")
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
        cur.execute(f"REPLACE INTO characters (name,gender,homeworld,height,mass,date) VALUES ('{resident_data['name']}','{resident_data['gender']}','{resident_data['homeworld']}','{resident_data['height']}','{resident_data['mass']}','{formatted_date}')")
        conn.commit()
#        print(cur.rowcount)
    print("----------------")

#import_planet()

def get_all_details_planet():
    cur = conn.cursor()
    cur.execute("SELECT * FROM planets")
    details_planet = cur.fetchall()

    cur.execute("SELECT * FROM characters")
    details_character = cur.fetchall()

    print(details_planet)
    print(details_character)

    return details_planet, details_character;

get_all_details_planet()


