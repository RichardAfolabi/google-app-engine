#
import os
import logging
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template


class MainHandler(webapp.RequestHandler):

	def get(self):
		path = self.request.path
		try:
			temp = os.path.join(
				os.path.dirname(__file__),
				'templates' + path)
			outstr = template.render(temp,
			{'greetings':'Hello guessman!'}, debug=True)
			self.response.out.write(str(outstr))


	def post(self):
		stguess = self.request.get('guess')

		try:
			guess = int(stguess)
		except:
			guess = -1

		# Initialize the number to guess
		answer = 42
		if guess == answer:
			msg = 'Congratulations'
		elif guess < 0:
			msg = 'Please provide a number guess'
		elif guess < answer:
			msg = 'Your answer is too low'
		else:
			msg = 'Your guess is too high'
			
		temp = os.path.join(
			os.path.dirname(__file__),
			'templates/index.html')
		outstr = template.render(temp,
		{'greetings':'hello guessman','stguess':stguess,'fdback':msg})
		self.response.out.write(str(outstr))


# Route all request with [www.domainname.com/].* to main handler. 
# Note . implies pattern matching any single character 
# while * implies zero or more occurence of the pattern to its left (i.e. '.')
# Hence, '.*' implies zero or more occurences of any single character.
# The main() says, “Create a new web application, and route all the
# URLs that come to this application (/.*) to the MainHandler class.


def main():
	application = webapp.WSGIApplication([
		('/.*', MainHandler)],
		debug=True)
	wsgiref.handlers.CGIHandler().run(application)

	
if __name__ == '__main__':
	main()
