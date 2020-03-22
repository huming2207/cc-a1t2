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
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
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
    student_id = ndb.StringProperty(indexed=False)
    name = ndb.StringProperty(indexed=False)
    password = ndb.IntegerProperty()


# [END greeting]


# [START main_page]
class MainPage(webapp2.RequestHandler):

    def get(self):
        student = StudentInfo(id="s3554025", name="Ming Hu", password=123456)
        student.put()

# [END main_page]


# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
# [END app]
