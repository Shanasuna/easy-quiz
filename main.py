#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import webapp2
import os
import jinja2
import json
from google.appengine.api import rdbms
from google.appengine.api import users
from apiclient.discovery import build
from oauth2client.appengine import OAuth2Decorator
from google.appengine.ext.webapp import template
from gaesessions import get_current_session
from gaesessions import SessionMiddleware
from login import Login
from apiclient import errors
from apiclient.http import MediaFileUpload

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    	extensions=['jinja2.ext.autoescape'],
	autoescape=True
)

INSTANCE_NAME = "gcdc2013-easyquiz:quiz1"
DATABASE = "quizdb"

decorator = OAuth2Decorator(
	client_id='811273628883-maqeqibrglovtamcnv6jdvijsfs5go2m.apps.googleusercontent.com',
        client_secret='ON_nhoYc613SI2WUJlHE8wL6',
	scope='https://www.googleapis.com/auth/drive'
)

service = build('drive', 'v2')

MIME_FOLDER = "application/vnd.google-apps.folder"
MIME_DOC = "application/vnd.google-apps.document"
MIME_SHEET = "application/vnd.google-apps.spreadsheet"
MIME_PRESENT = "application/vnd.google-apps.presentation"

class Main(webapp2.RequestHandler):
	@decorator.oauth_required
   	def get(self):
		checkLogin()
        	sql="select id, title, start from Quiz where owner=lower('%s') order by id asc"%(users.get_current_user().email().lower())
    		cursor.execute(sql)
		quiz = cursor.fetchall()
		con.close()

        	templates = {
			'username' : users.get_current_user(),
			'quiz' : quiz
		}
		get_template = JINJA_ENVIRONMENT.get_template('templates/index.html')
		self.response.write(get_template.render(templates))

class CreateQuiz(webapp2.RequestHandler):
	@decorator.oauth_required
   	def get(self):
		checkLogin()
        	templates = {
			'username' : users.get_current_user()		
		}
		get_template = JINJA_ENVIRONMENT.get_template('templates/add.html')
		self.response.write(get_template.render(templates))

class CreateQuizHandler(webapp2.RequestHandler):
	@decorator.oauth_required
   	def post(self):
		checkLogin()
		# title = self.request.get('title')
		# description = self.request.get('description')
		# start_date = self.request.get('start')
		# end_date = self.request.get('end')
		# location = self.request.get('location')

		data = json.loads(self.request.get('data'))
		title = data['title']
		description = data['description']
		start_date = data['startdate']
		end_date = data['enddate']
		location = data['location']

		con = rdbms.connect(instance=INSTANCE_NAME, database=DATABASE)
    		cursor = con.cursor()
        	sql="insert into Quiz (title, description, start, end, address, owner) values ('%s', '%s', '%s', '%s', '%s', '%s')"%(title, description, start_date, end_date, location, users.get_current_user().email().lower())
    		cursor.execute(sql)
		con.commit()

		sql="select id from Quiz where title='%s' and description='%s' and owner='%s' order by id desc limit 1"%(title, description, users.get_current_user().email().lower())
		cursor.execute(sql)
		zid = cursor.fetchall()[0][0]

		con.close()

		result = {
				'status' : 'OK',
				'id' : str(zid)
			}

		self.response.write(json.dumps(result))

		#self.redirect("/ModifyQuiz?id=" + zid)

class ModifyQuiz(webapp2.RequestHandler):
	@decorator.oauth_required
   	def get(self):
		checkLogin()
		zid = self.request.get('id')
		con = rdbms.connect(instance=INSTANCE_NAME, database=DATABASE)
    		cursor = con.cursor()
        	sql="select * from Quiz where id='%s'"%(zid)
    		cursor.execute(sql)
		quiz = cursor.fetchall()[0]
		con.close()

        	templates = {
			'username' : users.get_current_user(),
			'id' : quiz[0],
			'title' : quiz[1],
			'description' : quiz[2],
			'start' : quiz[4],
			'end' : quiz[5],
			'location' : quiz[6]
		}
		get_template = JINJA_ENVIRONMENT.get_template('templates/modify.html')
		self.response.write(get_template.render(templates))

class ModifyQuizHandler(webapp2.RequestHandler):
	@decorator.oauth_required
   	def post(self):
		checkLogin()
		# zid = self.request.get('id')
		# title = self.request.get('title')
		# description = self.request.get('description')
		# start_date = self.request.get('start')
		# end_date = self.request.get('end')
		# location = self.request.get('location')

		data = json.loads(self.request.get('data'))
		zid = data['id']
		title = data['title']
		description = data['description']
		start_date = data['startdate']
		end_date = data['enddate']
		location = data['location']

		con = rdbms.connect(instance=INSTANCE_NAME, database=DATABASE)
    		cursor = con.cursor()
        	sql="update Quiz set title='%s', description='%s', start='%s', end='%s', address='%s' where id='%s'"%(title, description, start_date, end_date, location, zid)
    		cursor.execute(sql)
		con.commit()
		con.close()

		result = {
			'status' : 'OK',
			'id' : str(zid)
		}

		self.response.write(json.dumps(result))

		#self.redirect('/')

class ManageQuestionHandler(webapp2.RequestHandler):
	@decorator.oauth_required
   	def post(self):
		checkLogin()
		# zid = self.request.get('id')
		# title = self.request.get('title')
		# description = self.request.get('description')
		# start_date = self.request.get('start')
		# end_date = self.request.get('end')
		# location = self.request.get('location')

		con = rdbms.connect(instance=INSTANCE_NAME, database=DATABASE)
    		cursor = con.cursor()

		zid = self.request.get('id')
		data = json.loads(self.request.get('data'))

		sql = "delete from Question where quiz_id='%s'"%(zid)
		cursor.execute(sql)
		con.commit()
		sql = "delete from Answer where quiz_id='%s'"%(zid)
		cursor.execute(sql)
		con.commit()

		for q in data:
			question = q['question']
			sql = "insert into Question (quiz_id, description) values ('%s', '%s')"%(zid, question)
			cursor.execute(sql)
			con.commit()
			
			sql = "select id from Question where quiz_id='%s' and description='%s' order by id desc limit 1"%(zid, question)
			cursor.execute(sql)
			qid = cursor.fetchall()[0][0]

			answer = q['answer']
			for a in answer:
				ans = a['answer']
				istrue = a['istrue']
				sql = "insert into Answer (quiz_id, question_id, title, is_true) values ('%s', '%s', '%s', %r)"%(zid, qid, ans, istrue)
				cursor.execute(sql)
				con.commit()


		result = {
			'status' : 'OK',
		}

		self.response.write(json.dumps(result))

class Quiz(webapp2.RequestHandler):
	@decorator.oauth_required
   	def get(self):
		checkLogin()
		zid = self.request.get('id')

		con = rdbms.connect(instance=INSTANCE_NAME, database=DATABASE)
    		cursor = con.cursor()

		sql="select title, description from Quiz where id='%s'"%(zid)
		cursor.execute(sql)
		row = cursor.fetchall()[0]
		title = row[0]
		description = row[1]

		sql = "select id, description from Question where quiz_id='%s'"%(zid)
		cursor.execute(sql)
		question_data = cursor.fetchall()
		questions = []
		for q in question_data:
			sql = "select id, title, is_true from Answer where question_id='%s'"%(q[0])
			cursor.execute(sql)
			answer_data = cursor.fetchall()
			answers = []
			for a in answer_data:
				answer = {
					'id' : a[0],
					'title' : a[1],
					'is_true' : a[2]
				}
				answers.append(answer)

			question = {
				'id' : q[0],
				'title' : q[1],
				'answers' : answers
			}
			questions.append(question)

        	templates = {
			'title' : title,
			'description' : description,
			'questions' : questions
		}
		#self.response.write(json.dumps(templates))
		get_template = JINJA_ENVIRONMENT.get_template('templates/quiz.html')
		self.response.write(get_template.render(templates))

class Test(webapp2.RequestHandler):
	@decorator.oauth_required
   	def get(self):
        	test_func(self, 1, 2)

class AnsQuiz(webapp2.RequestHandler):
	@decorator.oauth_required
   	def post(self): 
		checkLogin()
		session = get_current_session()
   		con = rdbms.connect(instance=INSTANCE_NAME, database=DATABASE)
    		cursor = con.cursor()
   		val = self.request.get('ans')
   		data = json.loads(val)
   		for ans in data:
   			ans['question'] = ans['question'].replace('question', '')
			sql="select q.quiz_id, a.id, a.is_true from Question q, Answer a where q.id='%s' and a.question_id='%s' and a.id='%s'"%(ans['question'], ans['question'], ans['ans'])
			cursor.execute(sql)
			row = cursor.fetchall()[0]
			sql="insert into AnsDB (quiz_id, question_id, ans_id, user_id, istrue) values ('%s', '%s', '%s', '%s', '%s')"%(row[0], ans['question'], row[1], str(session['user_id']), row[2])
			cursor.execute(sql)
			con.commit()

		self.response.write(val + ", UserID: " + str(session['user_id']))


app = webapp2.WSGIApplication([
	('/Test', Test),
    	('/', Main),
	('/Create', CreateQuiz),
	('/CreateQuizHandler', CreateQuizHandler),
	('/ModifyQuiz', ModifyQuiz),
	('/ModifyQuizHandler', ModifyQuizHandler),
	('/ManageQuestionHandler', ManageQuestionHandler),
	('/Quiz', Quiz),
	('/AnsQuiz', AnsQuiz),
	(decorator.callback_path, decorator.callback_handler())
], debug=True)
app = SessionMiddleware(app, cookie_key=str(os.urandom(64)))

def insert_file(self, service, title, description, parent_id, mime_type, filename):
  	#media_body = MediaFileUpload(filename, mimetype=mime_type, resumable=True)
  	body = {
    		'title': title,
    		'description': description,
    		'mimeType': mime_type
  	}
  	# Set the parent folder.
  	if parent_id:
    		body['parents'] = [{'id': parent_id}]

  	try:
    		file = service.files().insert(body=body).execute(http=decorator.http())

    		return file
  	except errors.HttpError, error:
    		self.response.write("An error occured: " + str(error) + ", " + str(errors.HttpError))
    		return None

def test_func(self, a, b):
	self.response.write(str(int(a)+int(b)))

def checkLogin():
	session = get_current_session()
	con = rdbms.connect(instance=INSTANCE_NAME, database=DATABASE)
	cursor = con.cursor()
	sql="select * from User where email='%s'"%(users.get_current_user().email().lower())
	cursor.execute(sql)
	row = cursor.fetchall()
	if not row:
		body = {
    			'title': "Easy Quiz",
    			'description': "EQ Description",
    			'mimeType': MIME_FOLDER
  		}
    		sql="insert into User (email, name) values ('%s', '%s')"%(users.get_current_user().email().lower(), users.get_current_user().nickname())
		cursor.execute(sql)
		con.commit()
		#result = insert_file(self, service, "Easy Quiz", "EQ Description", "", MIME_FOLDER, "")
		#file = service.files().insert(body=body).execute(http=decorator.http)
		#self.response.write("Self Link: " + result['selfLink'])
		#self.response.write("WebContent Link: " + result['webContentLink'])
		#self.response.write("WebView Link: " + result['webViewLink'])
		#self.response.write("Alternate Link: " + result['alternateLink'])
	#else:
		#self.response.write("Registered")

	sql="select id from User where email='%s' limit 1"%(users.get_current_user().email().lower())
	cursor.execute(sql)
	session['user_id'] = cursor.fetchall()[0][0]
