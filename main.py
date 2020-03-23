import os

from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.abspath('templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_STUDENT_INFO_NAME = 'default_student_info'


class StudentInfo(ndb.Model):
    name = ndb.StringProperty(indexed=False)
    password = ndb.IntegerProperty()


CURRENT_STUDENT = StudentInfo()


class MainPage(webapp2.RequestHandler):

    def get(self):
        global CURRENT_STUDENT
        student = StudentInfo(id="s3554025", name="Ming Hu", password=123456)
        student.put()

        student = StudentInfo(id="s35540251", name="Ming Hu A", password=234567)
        student.put()

        student = StudentInfo(id="s35540252", name="Ming Hu B", password=345678)
        student.put()

        login_status = {
            "student": CURRENT_STUDENT
        }

        print CURRENT_STUDENT
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(login_status))


class LoginHandler(webapp2.RequestHandler):

    def get(self):
        login_status = {
            "login_state": True
        }
        template = JINJA_ENVIRONMENT.get_template('login.html')
        self.response.write(template.render(login_status))

    def post(self):
        global CURRENT_STUDENT
        sid = str(self.request.get('id'))
        passwd = str(self.request.get('passwd'))

        student = StudentInfo.get_by_id(id=sid)

        if student is None or str(student.password) == passwd:
            CURRENT_STUDENT = student
            self.redirect('/')
        else:
            login_status = {
                "login_state": False
            }
            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(login_status))


class NameHandler(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('name.html')
        self.response.write(template.render())

    def post(self):
        global CURRENT_STUDENT
        student = CURRENT_STUDENT
        if student is None:
            return

        new_name = self.request.get('name')
        if len(new_name) < 1:
            name_status = {
                "invalid_name": True
            }
            template = JINJA_ENVIRONMENT.get_template('name.html')
            self.response.write(template.render(name_status))
        else:
            student.name = new_name
            student.put()
            CURRENT_STUDENT = student
            self.redirect("/")


class PasswordHandler(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('password.html')
        self.response.write(template.render())

    def post(self):
        student = CURRENT_STUDENT
        if student is None:
            return

        old_passwd = self.request.get('old-password')
        new_passwd = self.request.get('new-password')

        if str(student.password) == old_passwd:
            student.password = int(new_passwd)
            student.put()
            self.redirect('/login')
        else:
            password_status = {
                "invalid_password": True
            }
            template = JINJA_ENVIRONMENT.get_template('password.html')
            self.response.write(template.render(password_status))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/login', LoginHandler),
    ('/name', NameHandler),
    ('/password', PasswordHandler)
], debug=True)
