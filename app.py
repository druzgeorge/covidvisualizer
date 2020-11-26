from flask import Flask
from flask import render_template, url_for

import pycountry

from bs4 import BeautifulSoup

import requests
from requests.exceptions import HTTPError
app = Flask(__name__)
#globals are frowned upon
run_info = {'host':None}
if run_info['host'] == None:
    run_info['host'] = '127.0.0.1'
@app.route('/')
def index():
    return render_template('visualizer.html', host=run_info['host'])
@app.route('/info/<string:country_code>')
def info(country_code):
    #retrieving latest information on country
    code_len = len(country_code)
    # print(len(country_code))
    if code_len == 2:
        country_name = pycountry.countries.get(alpha_2=country_code)
    if code_len == 3:
        country_name = pycountry.countries.get(alpha_3=country_code)
    # print(country_name.name)
    # else:
    #     return 'An error occured determining ISO.Prolly has to do with the alpha_{country iso count}.Check that out!'
    # print(country_name)
    try:
        if str(country_code).lower == 'us':
            resp = requests.get(f'https://www.worldometers.info/coronavirus/country/us/')
        else:
            resp = requests.get(f'https://www.worldometers.info/coronavirus/country/{str(country_name.name).lower()}/')
            print('here')
        # print(resp.content)
    except HTTPError as e:
        print(e)
        return e
    soup = BeautifulSoup(resp.content, 'html.parser')
    counts = list(soup.find_all("div", id="maincounter-wrap"))
    #[0] = Cases, [1] = Deaths, [2]= recovered
    total_counts = list()
    for element in counts:
        # print('element')
        element = str(element).split('\n')
        # print(element)
        cnt = ''.join(filter(lambda i: i.isdigit(), element[3]))
        total_counts.append(cnt)
        # print(res)
        # print(str(element)[135:])
    # print(counts)
    return render_template('info.html', country_code=country_code, country_name=country_name, counts=total_counts)
if __name__ == '__main__':
    app.run(debug=True,host=run_info['host'])