"""
@author: Denis Z
2022
"""

import requests
import json
import pymysql
from datetime import datetime
import variables

#Creating a connection to the database
conn = pymysql.connect(
    host=variables.host,
    port=variables.port,
    user=variables.user,
    password=variables.password,
    db=variables.database,
)


def import_planet(name):
    """
    Add planet and its residents to the database
    """
    url = name
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

    response = requests.get(url, headers={'Accept': 'application/json'}, params={format: json})
    data = response.json()

    cur = conn.cursor()
    cur.execute(f"REPLACE INTO planets (name,gravity,climate,terrain,population,url,date) VALUES ('{data['name']}',"
                f"'{data['gravity']}','{data['climate']}','{data['terrain']}','{data['population']}','{data['url']}',"
                f"'{formatted_date}')")
    # Saving transaction
    conn.commit()

    planet_name = data['name']
    ins_planet = cur.rowcount

    for resident in data['residents']:
        resident_url = resident
        resident_response = requests.get(resident_url, headers={'Accept': 'application/json'}, params={format: json})
        resident_data = resident_response.json()

        cur = conn.cursor()
        cur.execute(f"REPLACE INTO characters (name,gender,homeworld,height,mass,date) "
                    f"VALUES ('{resident_data['name']}','{resident_data['gender']}','{resident_data['homeworld']}',"
                    f"'{resident_data['height']}','{resident_data['mass']}','{formatted_date}')")
        #Saving transaction
        conn.commit()

    return planet_name, ins_planet


def delete_planet(name_delete):
    """
    Delete planet and its residents from the database
    """
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM planets WHERE (url = '{name_delete}')")
    name_del_planet = cur.fetchall()[0][1]

    cur.execute(f"DELETE FROM planets WHERE (url = '{name_delete}')")
    del_planet = cur.rowcount

    cur.execute(f"DELETE FROM characters WHERE (homeworld = '{name_delete}')")

    # Saving transaction
    conn.commit()

    return name_del_planet, del_planet



def get_all_details_planet():
    """
    Getting data from the database
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM planets")
    details_planet = cur.fetchall()

    cur.execute("SELECT * FROM characters")
    details_character = cur.fetchall()

    return details_planet, details_character




