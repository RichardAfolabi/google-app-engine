#
import os
import logging
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template




def doRender(handler, tname='index.html', values={}):
    #Check if the template file tname exists

    temp = os.path.join(os.path.dirname(__file__),
         'template/' + tname)
    if not os.path.isfile(temp):
        return False


    # If template file exisis, make a copy and add the path
    newval = dict(values)
    newval['path'] = handler.request.path

    outstr = template.render(temp, newval)
    handler.response.out.write(str(outstr))
    return True



class LoginHandler(webapp.RequestHandler):

    def get(self):
        doRender(self, 'loginscreen.html')


    def post(self):
        acct = self.request.get('account')
        pw = self.request.get('password')
        logging.info('Checking account = '+acct+' pw='+pw)

        if pw == '' or acct == '':
            doRender(self, 'loginscreen.html', {'error': 'Please specify Account and Password'} )
        elif pw == 'secret':
            doRender(self, 'loggedin.html', {'greetn':'Welcome, '+acct})
        else:
            doRender(self, 'loginscreen.html', {'error': 'Incorrect password'} )




class MainHandler(webapp.RequestHandler):

    def get(self):
        if doRender(self, self.request.path):
            return
        doRender(self, 'index.html')




def main():
    application = webapp.WSGIApplication([
        ('/login', LoginHandler),
        ('/.*', MainHandler)],
        debug=True)
    wsgiref.handlers.CGIHandler().run(application)

    
if __name__ == '__main__':
    main()
