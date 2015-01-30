from flask import render_template, request
from app import app
import pymysql as mdb
import json
#read credentialfile
inobj = open( 'credentials.json', 'r')
credentials = json.load(inobj)
db= mdb.connect(user=credentials['user'], password=credentials['password'],host="localhost", db="materials_project", charset='utf8')

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')
    #return "Hello World"
    
@app.route('/return_page', methods=['GET'])
def return_page():
    name = request.args.get('name', None)
    #return_val = {'id1':'somevalue'}
    with db:
        cur= db.cursor()
        cur.execute("SELECT CASE WHEN material1 = '%s' then material2 else material1 END AS material, value from analysis_results where '%s' in (material1,material2) and type='n_euclid_sprse' order by value asc limit 10" % (name, name))
        query_results = cur.fetchall()
        return_val = []
        for result in query_results:
            return_val.append(dict(material=result[0], n_euclid_sprse=result[1]))
    return render_template( 'return_page.html', name=name,return_val =return_val)