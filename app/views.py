from flask import render_template, request
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')
    #return "Hello World"
    
@app.route('/return_page', methods=['GET'])
def return_page():
    name = request.args.get('name', None)
    #return_val = {'id1':'somevalue'}
    return_val = ['SnNa', 'YbSn']
    return render_template( 'return_page.html', name=name,return_val =return_val)