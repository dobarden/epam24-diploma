"""
@author: Denis Z
2022
"""

from flask import Flask, render_template, request
from markupsafe import Markup
import rds_db as db_sw

app = Flask(__name__)

@app.route('/')
def index():
    all_planets, all_characters = db_sw.get_all_details_planet()
    br = "<br>\n"
    br = Markup(br)
    all_data = ""
    form_items_for_del = "<option disabled selected>---Planets to delete---</option>"
    for item in all_planets:
        planet_items = '<h2>Planet ' + item[1] + ' and its residents: </h2><ul>'
        planet_items += '<li> Name: ' + item[1] + '</li>'
        planet_items += '<li> Gravity: ' + item[2] + '</li>'
        planet_items += '<li> Climate: ' + item[3] + '</li>'
        planet_items += '<li> Terrain: ' + item[4] + '</li>'
        planet_items += '<li> Population: ' + str(item[5]) + '</li>'
        planet_items += '<li> Added/Updated: ' + item[7] + '</li>'
        planet_items += '</ul>'
        planet_items = Markup(planet_items)
        all_data = all_data + planet_items
        form_items_for_del += '<option value="' + item[6] + '">' + item[1] + '</option>'

        planet_residents = ''
        for character in all_characters:
            if character[3] == item[6]:
                planet_residents += '<tr>'
                planet_residents += '<td><b>' + character[1] + '</b></td>'
                planet_residents += '<td>' + character[2] + '</td>'
                planet_residents += '<td>' + str(character[4]) + '</td>'
                planet_residents += '<td>' + character[5] + '</td>'
                planet_residents += '<td>' + character[6] + '</td>'
                planet_residents += '</tr>'
        planet_residents = '<table><tr style="background-color:#C1C1C1"><th>Name</th><th>Gender</th><th>Height</th><th>Mass</th><th>Added/Updated</th></tr>' + planet_residents + '</table><br>'
        planet_residents = Markup(planet_residents)
        all_data = all_data + planet_residents
    form_items_for_del = Markup(form_items_for_del)

    return render_template('index.html', var=all_data, form_items_for_del=form_items_for_del)


@app.route('/insert', methods=['post'])
def insert():
    if request.method == 'POST':
        form_input_select = request.form['name']
        form_input_text = request.form['form_input_text']

        if not form_input_text:
            planet_url = form_input_select
        else:
            planet_url = form_input_text

        ins_planet = db_sw.import_planet(planet_url)
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

