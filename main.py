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
	client_id='981805140817.apps.googleusercontent.com',
        client_secret='YT2KhOg3nPgXUeV60wA3iAwS',
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
			#result = insert_file(self, service, "Easy Quiz", "EQ Description", "", MIME_FOLDER, "")
			#file = service.files().insert(body=body).execute(http=decorator.http)
			#self.response.write("Self Link: " + result['selfLink'])
			#self.response.write("WebContent Link: " + result['webContentLink'])
			#self.response.write("WebView Link: " + result['webViewLink'])
			#self.response.write("Alternate Link: " + result['alternateLink'])
		#else:
			#self.response.write("Registered")

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
        	templates = {
			'username' : users.get_current_user()		
		}
		get_template = JINJA_ENVIRONMENT.get_template('templates/add.html')
		self.response.write(get_template.render(templates))

class CreateQuizHandler(webapp2.RequestHandler):
	@decorator.oauth_required
   	def post(self):
		title = self.request.get('title')
		description = self.request.get('description')
		start_date = self.request.get('start')
		end_date = self.request.get('end')
		location = self.request.get('location')

		con = rdbms.connect(instance=INSTANCE_NAME, database=DATABASE)
    		cursor = con.cursor()
        	sql="insert into Quiz (title, description, start, end, address, owner) values ('%s', '%s', '%s', '%s', '%s', '%s')"%(title, description, start_date, end_date, location, users.get_current_user().email().lower())
    		cursor.execute(sql)
		con.commit()
		con.close()

		self.redirect('/')

class ModifyQuiz(webapp2.RequestHandler):
	@decorator.oauth_required
   	def get(self):
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
		zid = self.request.get('id')
		title = self.request.get('title')
		description = self.request.get('description')
		start_date = self.request.get('start')
		end_date = self.request.get('end')
		location = self.request.get('location')

		con = rdbms.connect(instance=INSTANCE_NAME, database=DATABASE)
    		cursor = con.cursor()
        	sql="update Quiz set title='%s', description='%s', start='%s', end='%s', address='%s' where id='%s'"%(title, description, start_date, end_date, location, zid)
    		cursor.execute(sql)
		con.commit()
		con.close()

		self.redirect('/')

class Quiz(webapp2.RequestHandler):
	@decorator.oauth_required
   	def get(self):
        	templates = {			
		}
		get_template = JINJA_ENVIRONMENT.get_template('main.html')
		self.response.write(get_template.render(templates))

class Test(webapp2.RequestHandler):
	@decorator.oauth_required
   	def get(self):
        	test_func(self, 1, 2)


app = webapp2.WSGIApplication([
	('/Test', Test),
    	('/', Main),
	('/Create', CreateQuiz),
	('/CreateQuizHandler', CreateQuizHandler),
	('/ModifyQuiz', ModifyQuiz),
	('/ModifyQuizHandler', ModifyQuizHandler),
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

