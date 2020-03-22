from google.appengine.ext import ndb


class StudentInfo(ndb.Model):
    id = ndb.KeyProperty(),
    name = ndb.StringProperty(indexed=False),
    password = ndb.StringProperty(indexed=False),
