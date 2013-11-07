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
from google.appengine.api import users
from apiclient.discovery import build
from oauth2client.appengine import OAuth2Decorator
from google.appengine.ext.webapp import template
from gaesessions import get_current_session
from gaesessions import SessionMiddleware
from login import Login

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    	extensions=['jinja2.ext.autoescape']
)

decorator = OAuth2Decorator(
	client_id='485793544323-r7jnme7rj0prdo07ml5mcndcbmkcm6du.apps.googleusercontent.com',
        client_secret='QZBgK4wgujNsxhsY_haPJeqO',
	scope='https://www.googleapis.com/auth/drive'
)

service = build('drive', 'v2')

class Main(webapp2.RequestHandler):
	@decorator.oauth_required
   	def get(self):

		

        	templates = {			
		}
		get_template = JINJA_ENVIRONMENT.get_template('main.html')
		self.response.write(get_template.render(templates))

class CreateQuiz(webapp2.RequestHandler):
	@decorator.oauth_required
   	def get(self):
        	templates = {			
		}
		get_template = JINJA_ENVIRONMENT.get_template('main.html')
		self.response.write(get_template.render(templates))

class Quiz(webapp2.RequestHandler):
	@decorator.oauth_required
   	def get(self):
        	templates = {			
		}
		get_template = JINJA_ENVIRONMENT.get_template('main.html')
		self.response.write(get_template.render(templates))

class CreateQuiz(webapp2.RequestHandler):
	@decorator.oauth_required
   	def get(self):
        	templates = {			
		}
		get_template = JINJA_ENVIRONMENT.get_template('main.html')
		self.response.write(get_template.render(templates))

class CreateQuiz(webapp2.RequestHandler):
	@decorator.oauth_required
   	def get(self):
        	templates = {			
		}
		get_template = JINJA_ENVIRONMENT.get_template('main.html')
		self.response.write(get_template.render(templates))

class CreateQuiz(webapp2.RequestHandler):
	@decorator.oauth_required
   	def get(self):
        	templates = {			
		}
		get_template = JINJA_ENVIRONMENT.get_template('main.html')
		self.response.write(get_template.render(templates))


app = webapp2.WSGIApplication([
    	('/', Main),
	('/Login', Login),
	(decorator.callback_path, decorator.callback_handler())
], debug=True)
app = SessionMiddleware(app, cookie_key=str(os.urandom(64)))
