#TODO url location check
#TODO testy!!
#TODO dokumentace
import re
from flask import Flask
from flask.ext.restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

CALENDARS = [		]


def comapreDates(day1, month1, year1, day2,month2, year2):
	if year1 == year2:
		if month1 == month2:
			if day1 >= day2:
				return True
			else:
				return False
			
		elif month1 > month2:
			return True
		else: 
			return False
	elif year1 > year2:
		return True
	else:
		return False
def dateCheck(date):
	b = re.match("^([0-2][0-9]|[3][01]){1}-([0][1-9]|[1][0-2]){1}-[0-9]{4}$", date, flags=0)
	if not b:
		abort(400, message="Date's format is not valid")
	
	days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	
	day = int(date[:2])
	month = int(date[3-5])
	year = int(date[-4:])
	
	
		
	if (day > days[month]):
		if month == 1:
			cond1 = year % 4 # == 0
			cond2 = year % 100 # != 0 
			cond3 = year % 400 #== 0
			
			if ((((cond1 == 0) and (cond2 != 0)) or (cond3 == 0)) and day <= 29):
				return True
		abort(400, message="This date doesn't exist")
	
	

def clockFormatCheck(clock):
	b = re.match("^([01][0-9]|[2][0-3]){1}:[0-5][0-9]$", clock, flags=0)
	if not b:
		abort(400, message="Clock's format is not valid")
def repFormatCheck(repeat):
	b = re.match("^[0-9]*$", repeat, flags=0)
	if not b:
		abort(400, message="Repeat's format is not valid")


def calendar_exist_check(calendar):
	if calendar >= len(CALENDARS):
		abort(404, message="Calendar {} doesn't exist".format(calendar))

def entry_exist_check(calendar, entry):
	calendar_exist_check(calendar)
	if not(entry in CALENDARS[calendar]): 
		abort(404, message="Entry {} doesn't exist".format(calendar))

def checkArgs(args):	
	if args['date'] is not None:
		dateCheck(args['date'])
	if args['from'] is not None:
		clockFormatCheck(args['from'])
	if args['to'] is not None:
		clockFormatCheck(args['to'])		
	if args['repeats'] is not None:
		repFormatCheck(args['repeats'])
	
	
rangeParser = reqparse.RequestParser()
rangeParser.add_argument('from', type=str, required = False)
rangeParser.add_argument('to', type=str, required = False)


entryModifedParser = reqparse.RequestParser()
entryModifedParser.add_argument('date', type=str, required = False)
entryModifedParser.add_argument('from', type=str, required = False)
entryModifedParser.add_argument('to', type=str, required = False)
entryModifedParser.add_argument('description', type=str, required=False)
entryModifedParser.add_argument('repeats', type=str, required=False)
entryModifedParser.add_argument('location', type=str, required=False)

entryParser = reqparse.RequestParser()
entryParser.add_argument('date', type=str, required=True)
entryParser.add_argument('from', type=str, required=True)
entryParser.add_argument('to', type=str, required=True)
entryParser.add_argument('description', type=str, required=True)
entryParser.add_argument('repeats', type=str, required=False)
entryParser.add_argument('location', type=str, required=False)

class Entry(Resource):
	def get(self, calendar_id, entry_id): #
		entry_exist_check(calendar_id, entry_id)
		return CALENDARS[calendar_id][entry_id]
	def put(self, calendar_id, entry_id):
		entry_exist_check(calendar_id, entry_id)
		
		args = entryModifedParser.parse_args()
		
		for key in args.keys():
			if (key in CALENDARS[calendar_id][entry_id]) and (args[key] is not None):
				CALENDARS[calendar_id][entry_id][key] = args[key]
				
		return CALENDARS[calendar_id][entry_id]
		
	def delete(self, calendar_id, entry_id):
		entry_exist_check(calendar_id, entry_id)
		del CALENDARS[calendar_id][entry_id]
		return '', 204




class Calendar(Resource):
	def get(self, index):
		args = rangeParser.parse_args()
		calendar_exist_check(index)
		from_date = ''
		to_date = ''
		
		if 'from' in args:
			if args['from'] is not None:
				dateCheck(args['from'])
				from_date = args['from']	
		if 'to' in args:
			if args['to'] is not None:
				dateCheck(args['to'])
				to_date = args['to']
		
		result = {}
		
		if to_date != '' or from_date != '':
			for key in CALENDARS[index]:
				if (to_date != ''):
					to_day = int(to_date[:2])
					to_month = int(to_date[3:5])
					to_year = int(to_date[-4:])
				
				if (from_date != ''):
					from_day = int(from_date[:2])
					from_month = int(from_date[3:5])
					from_year = int(from_date[-4:])
				
				repeats = int(CALENDARS[index][key]['repeats'])
				this_day = int(CALENDARS[index][key]['date'][:2])
				
				for x in range(0, repeats + 1):
					
					this_month = (int(CALENDARS[index][key]['date'][3:5]) + x) % 12
					this_year = int(CALENDARS[index][key]['date'][-4:]) + ((this_month + x) / 12)
					
					to_this = (to_date != '' and comapreDates(to_day, to_month, to_year, this_day, this_month, this_year))
					from_this = (from_date != '' and comapreDates(this_day, this_month, this_year, from_day, from_month, from_year))
					
					
					if (from_date == '' and to_date != '' and to_this is True) or (from_date != '' and to_date == '' and from_this is True) or (from_this is True and to_this is True):
						result[key] = CALENDARS[index][key]
		
		else:
			return CALENDARS[index]
		return result

	#creating entry
	def post(self, index):
		calendar_exist_check(index)
		args = entryParser.parse_args()
		checkArgs(args)
		entry_id = len(CALENDARS[index]) + 1
		CALENDARS[index][entry_id] = args
		if CALENDARS[index][entry_id]['location'] is None:
			CALENDARS[index][entry_id]['location'] = ""
		if CALENDARS[index][entry_id]['repeats'] is None:
			CALENDARS[index][entry_id]['repeats'] = "0"
				
		return CALENDARS[index][entry_id], 201
	#reinitialization of calendar
	def delete(self, index):
		calendar_exist_check(index)
		del CALENDARS[index]
		return '', 204
	


class CalendarList(Resource): 
	def get(self):
		return CALENDARS
	def post(self):
		calendar_id = len(CALENDARS)
		CALENDARS.append({})
		return CALENDARS[calendar_id], 201
	
		
##
## Actually setup the Api resource routing here
##x

api.add_resource(CalendarList, '/')
api.add_resource(Calendar, '/<int:index>')
api.add_resource(Entry, '/<int:calendar_id>/<int:entry_id>')


if __name__ == '__main__':
    app.run(debug=True)