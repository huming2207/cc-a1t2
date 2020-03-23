#!/usr/bin/env python

# Copyright 2016 Google Inc.
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

# [START imports]
import json
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.abspath('templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

DEFAULT_STUDENT_INFO_NAME = 'default_student_info'


# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent. However, the write rate should be limited to
# ~1/second.

def student_info_key(guestbook_name=DEFAULT_STUDENT_INFO_NAME):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('Students', guestbook_name)


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
            CURRENT_STUDENT = StudentInfo()
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

    def post(self):
        student = CURRENT_STUDENT
        if student is None:
            return

        old_passwd = self.request.get('old_passwd')
        new_passwd = self.request.get('new_passwd')

        if str(student.password) == old_passwd:
            student.password = int(new_passwd)
            self.response.delete_cookie(key='user_id')
            self.response.delete_cookie(key='user_name')
            self.redirect('/login')
        else:
            self.response.set_status(403)
            obj = {'message': 'Password is invalid or not logged in'}
            self.response.write(json.dumps(obj))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/login', LoginHandler),
    ('/name', NameHandler),
    ('/password', PasswordHandler)
], debug=True)
