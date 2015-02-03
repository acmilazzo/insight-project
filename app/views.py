from flask import render_template, request
from app import app
import pymysql as mdb
import json
#read credentialfile
inobj = open( 'credentials.json', 'r')
credentials = json.load(inobj)
db= mdb.connect(user=credentials['user'], password=credentials['password'],host=credentials['host'], db=credentials['db'], charset='utf8')

@app.route('/')
def titlepage():
    return render_template('titlepage.html',title='Home')
    
@app.route('/index')
def index():
    return render_template('index.html', title='Demo')
    
@app.route('/return_page', methods=['GET'])
def return_page():
    name = request.args.get('name', None)
    #return_val = {'id1':'somevalue'}
    with db:
        cur= db.cursor()
        cur.execute( "SELECT CASE WHEN a1.material1 = '%s' then a1.material2 else a1.material1 END AS material, a1.value FROM analysis_results a1 join analysis_results a2 on a1.material1 = a2.material1 and a1.material2 = a2.material2 and a2.type = 'num_feat_sprse' WHERE '%s' in (a1.material1,a1.material2) and a1.type='n_euclid_sprse' and a2.value > 3 ORDER by a1.value asc limit 5" % (name, name))
        query_results = cur.fetchall()
        return_val = []
        for result in query_results:
            return_val.append(dict(material=result[0], n_euclid_sprse=result[1]))
    return render_template( 'return_page.html', name=name,return_val =return_val)
@app.route('/slides')
def slides():
    return render_template('slides.html', title='Slides')