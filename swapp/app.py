"""
@author: Denis Z
2022
"""
import socket
from flask import Flask, render_template, request
from markupsafe import Markup
import aws_mysql_db as db1

app = Flask(__name__)

#Initially adding planets with URLs and tables to the database
@app.before_first_request
def before_first_request_func():
    db1.init_import_planetsurls()

#Homepage
@app.route('/')
def index():

    all_planets, all_characters = db1.get_all_details_planet()
    all_planets_urls = db1.get_planets_urls()
    all_data, form_items_for_del, form_planets_urls = main_output(all_planets, all_characters, all_planets_urls)
    if not all_data:
        all_data = '<h2 style="color: red; text-align: center; padding-top: 30px;">No planets in the database!</h2>'
        all_data = Markup(all_data)
    ip_addr = server_ip()
    return render_template('index.html', var=all_data, form_items_for_del=form_items_for_del,
                           ip_addr=ip_addr, form_planets_urls=form_planets_urls)


#Adding data to the database
@app.route('/insert', methods=['post'])
def insert():

    if request.method == 'POST':
        form_input_select = request.form['form_select_planet']
        form_input_text = request.form['form_input_text']

        if not form_input_text:
            planet_url = form_input_select
        else:
            planet_url = form_input_text

        planet_name, ins_planet = db1.import_planet(planet_url)

        if ins_planet == 1:
            planet_addel = "added"
        else:
            planet_addel = "updated"

        all_planets, all_characters = db1.get_all_details_planet()
        all_planets_urls = db1.get_planets_urls()
        all_data, form_items_for_del, form_planets_urls = main_output(all_planets, all_characters, all_planets_urls)
        ip_addr = server_ip()

        return render_template('index.html', var=all_data, addel_planet=planet_addel, planet_name=planet_name,
                               form_items_for_del=form_items_for_del, ip_addr=ip_addr, form_planets_urls=form_planets_urls)


#Deleting planet from the database
@app.route('/delete', methods=['post'])
def delete():

    if request.method == 'POST':
        name_delete = request.form['name_delete']
        name_del_planet, del_planet = db1.delete_planet(name_delete)
        if del_planet == 1:
            planet_addel = "deleted"
        else:
            planet_addel = "NOT deleted"

        all_planets, all_characters = db1.get_all_details_planet()
        all_planets_urls = db1.get_planets_urls()
        all_data, form_items_for_del, form_planets_urls = main_output(all_planets, all_characters, all_planets_urls)
        ip_addr = server_ip()

        return render_template('index.html', var=all_data,  addel_planet=planet_addel, planet_name=name_del_planet,
                               form_items_for_del=form_items_for_del, ip_addr=ip_addr, form_planets_urls=form_planets_urls)

#Obtain the Server IP

def server_ip():
    ip_addr = socket.gethostbyname(socket.gethostname())
    return ip_addr


#Prepairing output for frontend
def main_output(all_planets, all_characters, all_planets_urls):
    all_data = ""
    form_items_for_del = ""
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
        if not planet_residents:
            planet_residents = '<b style="color: red;">NO RESIDENTS!!!</b><br>'
        else:
            planet_residents = '<table><tr style="background-color:#C1C1C1"><th>Name</th><th>Gender</th><th>Height</th>' \
                               '<th>Mass</th><th>Added/Updated</th></tr>' + planet_residents + '</table><br>'
        planet_residents = Markup(planet_residents)
        all_data = all_data + planet_residents
    form_items_for_del = Markup(form_items_for_del)

    form_planets_urls = ""
    for item in all_planets_urls:
        form_planets_urls += '<option value="' + item[2] + '">' + item[1] + '</option>'
    form_planets_urls = Markup(form_planets_urls)

    return all_data, form_items_for_del, form_planets_urls


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)