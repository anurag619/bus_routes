from flask import jsonify
import re
import requests
from flask import Flask, jsonify, request, render_template, json

app = Flask(__name__, static_folder='static', template_folder= 'templates')
app.secret_key= '\xbf\xb50\x94au\x8f\xf9\se2\x1f\x93\x06(\xdf\xe4\xaf\x1f\x86k\xb3\x2fQ%1'


@app.route('/')
def home():

	return render_template('home.html')


@app.route('/about')
def about():

	return render_template('about.html')

@app.route('/search')
def search():

	data = requests.get('http://routes1.herokuapp.com/')

	binary = data.content
	output = json.loads(binary)

	from_list = []
	to_list = []
	
	for i in output['start']:
		from_list.append(i)


	return render_template('options.html', from_data = from_list )


@app.route('/input', methods=('GET' ,'POST') )
def sorted():
	if request.method=='POST':
		start = request.form['from']
		end = request.form['to']

		url = 'http://routes1.herokuapp.com/%s/%s' %(start,end)
		data = requests.get(url)
		binary = data.text
		binary = eval(binary)
		num = binary['number']


	return render_template('index.html', result=num, start=start,end=end)

@app.route('/edit', methods=('GET' ,'POST') )
def edit():

	if request.method=='POST':
		
		start = request.form['starts'] 
		end = request.form['end']
		number = request.form['number']
		bus_type = request.form['type']
		passes = request.form['via']  

		new = request.form.getlist('check')
		edit = request.form.getlist('check')

		if new:
			payload = {'start': start, 'end': end, 'number':number, 'type': bus_type, 'passes':passes, 'data': str(new[0] )}
		elif edit:
			payload = {'start': start, 'end': end, 'number':number, 'type': bus_type, 'passes':passes, 'data': str(edit[0] )}

		resp = requests.post("http://userdata.herokuapp.com/home", data=payload)

		binary = resp.content
		output = json.loads(binary)
		
		res= output['mess']

		if res == 'ok':
			return render_template('edit.html', status= '200' )

		

	return render_template('edit.html')

@app.route('/rules', methods=('GET' ,'POST') )
def rules():

	return render_template('rules.html')


	

if __name__ == '__main__':
	app.run(debug=True)
