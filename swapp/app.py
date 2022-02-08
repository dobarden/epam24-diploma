"""
@author: Denis Z
2022
"""

from flask import Flask, render_template, request
from markupsafe import Markup

app = Flask(__name__)

import rds_db as db_sw


@app.route('/')
def index():
    all_planets, all_characters = db_sw.get_all_details_planet()
    br = "<br>\n"
    br = Markup(br)
    all_data = ""
    for item in all_planets:
        all_data = all_data + str(item) + br
        for character in all_characters:
            if character[3] == item[6]:
                all_data = all_data + str(character) + br
        all_data = all_data + br + br
    return render_template('index.html', var=all_data)


@app.route('/insert', methods=['post'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
#        db_sw.import_planet(name)
        ins_planet = db_sw.import_planet(name)
        if ins_planet == 1:
            planet_addel = "Added"
        else:
            planet_addel = "Updated"
        all_planets, all_characters = db_sw.get_all_details_planet()
        br = "<br>\n"
        br = Markup(br)
        all_data = ""
        for item in all_planets:
            all_data = all_data + str(item) + br
            for character in all_characters:
                if character[3] == item[6]:
                    all_data = all_data + str(character) + br
            all_data = all_data + br + br

        return render_template('index.html', var=all_data, addel_planet=planet_addel)

@app.route('/delete', methods=['post'])
def delete():
    if request.method == 'POST':
        name_delete = request.form['name_delete']
        del_planet = db_sw.delete_planet(name_delete)
#        ins_planet = db_sw.delete_planet(name_delete)
#        if ins_planet == 1:
#            planet_addel = "Added"
#        else:
#            planet_addel = "Updated"

        if del_planet == 1:
            planet_addel = "Deleted"

        all_planets, all_characters = db_sw.get_all_details_planet()
        br = "<br>\n"
        br = Markup(br)
        all_data = ""
        for item in all_planets:
            all_data = all_data + str(item) + br
            for character in all_characters:
                if character[3] == item[6]:
                    all_data = all_data + str(character) + br
            all_data = all_data + br + br

        return render_template('index.html', var=all_data,  addel_planet=planet_addel)



if __name__ == "__main__":
    app.run(debug=True)

