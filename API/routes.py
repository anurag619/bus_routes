from flask.ext.mongoengine import MongoEngine

from mongoengine import *

from flask import Flask, jsonify, request
app = Flask(__name__)

app.secret_key = 'something secret'

DB_NAME = 'name'
DB_USERNAME = 'user'
DB_PASSWORD = 'password'
DB_HOST_ADDRESS = 'get-host-address-from-mongolab.com'

app.config["MONGODB_DB"] = DB_NAME
connect(DB_NAME, host='mongodb://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOST_ADDRESS)

db = MongoEngine(app)

class Bus(db.Document):
	key = db.IntField()
	start = db.StringField(max_length=35)
	end = db.StringField(max_length=35)
	number = db.DynamicField()
	bus_type = db.StringField(max_length=25)

	via = db.ListField(db.EmbeddedDocumentField('Route'))

	def __repr__(self):
		return '<key %r, num %r>' % (self.key, self.number)


class Route(db.EmbeddedDocument):
	passes = db.StringField(max_length=30, required = True)



@app.route('/', methods=['GET'])
def home():
	starts = []
	ends =[]
	for i in Bus.objects:
		
		starts.append(i.start)
		starts.append(i.end)

		ends.append(i.end)
		ends.append(i.start)

	starts = list(set(starts))
	ends = list(set(ends))

	return jsonify({ 'start': starts, 'end': ends })

@app.route('/<start>/<to>', methods=['GET'])
def input(start,to):
	if request.method=='GET':
		
		via = []
		result = []

		for j in Bus.objects:

			if start in j.start and to in j.end:
				
				result.append(j.number)
			options = []

			for k in j.via:
				options.append(k)

			if start in options and to in j.start :
				
				result.append(j.number)

			if start in j.start and to in options:
				result.append(j.number)
			
			if start in options and to in j.end :
				
				result.append(j.number)

			if start in j.end and to in options:
				result.append(j.number)

	return jsonify({ 'number': result


		})

if __name__ == '__main__':
  app.run(debug=True)