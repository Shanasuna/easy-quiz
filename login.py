import webapp2

class Login(webapp2.RequestHandler):
    	def get(self):
        	self.response.write('Login Page')

