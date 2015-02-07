from flask import render_template, request
from app import app
import pymysql as mdb
import json

#read credentialfile
inobj = open( 'credentials.json', 'r')
credentials = json.load(inobj)

@app.route('/')
def titlepage():
    return render_template('titlepage.html',title='Home')
    
@app.route('/index')
def index():
    return render_template('index.html', title='Demo')
    
@app.route('/return_page', methods=['GET'])
def return_page():
    name = request.args.get('name', None)
    db = mdb.connect(user=credentials['user'], 
    password=credentials['password'],
    host=credentials['host'], 
    db=credentials['db'], charset='utf8')
    
    with db:
        cur= db.cursor()
        cur.execute( """SELECT CASE WHEN material1 = '%s'
                            THEN material2 ELSE material1 END
                            AS material, cosine, n_euclid, ktau
                            FROM analysis
                            WHERE '%s' in (material1,material2)
                              and num_feat > 3
                            ORDER BY n_euclid asc limit 5""" %(name, name))
        
        query_results = cur.fetchall()
        return_val = []
        for result in query_results:
            sprse_val = round( result[2], 3 )
            cosine_val = round( result[1], 3 )
            corr_val = round( result[3], 3 )
            return_val.append(dict(material=result[0], 
                              n_euclid_sprse=sprse_val, 
                              cosine=cosine_val, correlation=corr_val))
    	cur.close()
    db.close()
    if len(return_val) >=1 :
        return render_template( 'return_page.html', name=name,return_val =return_val)
    else:
        return render_template( 'return_page.html', name=name)

@app.route('/slides')
def slides():
    return render_template('slides.html', title='Slides')
