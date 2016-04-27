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
import os
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.ext import ndb

class Message(ndb.Model):
    content = ndb.StringProperty()

def save_message_and_generate_id(message):
    data = Message(content=message)
    key = data.put()
    return key.id()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, None))

class MessageHandler(webapp2.RequestHandler):

    def post(self):
        content = self.request.params['content']
        link = "http://{host}/{id}".format(
            host=self.request.host, id=save_message_and_generate_id(content))

        self.response.write(link)

class DisplayHandler(webapp2.RequestHandler):

    def get(self, key):
        user_agent = self.request.headers['User-Agent']

        print user_agent

        # Don't exhaust the message if it's just Skype looking for a preview.
        if "SkypeUriPreview" in user_agent:
            self.response.write("Skype is not allowed to see the message.")
            return

        message = Message.get_by_id(int(key))
        if message:
            self.response.write(message.content)
            message.key.delete()
        else:
            self.response.write("Cannot find message.")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/message', MessageHandler),
    ('/(\d+)', DisplayHandler),
], debug=True)
