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
import cgi
import re, os

class BaseHandler(webapp2.RequestHandler):
    def render(self, textarea, **kw):
        self.response.out.write(render_str(textarea, **kw))

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r'^[\S]@[\S]+\[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Signup(BaseHandler):

    def get(self):
        self.render("signup-form.html")

    def post(self):
        have_error = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email =self.request.get("email")

        params = dict(username = username,
                        email = email)

        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That's not a valid password"
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match"
            have_error = True

        if not valid_email(email):
            params['error_mail'] = "That's not a valid email"
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            self.redirect('/welcome.html?username=' + username)

class Welcome(BaseHandler):
    def get(self):
        username =self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username = username)
        else:
            self.redirect('/signup-form.html')

def build_page(textarea_content):
    user_label = "<label>Usename</label>"
    user_input = "<input type=name/>"
    textarea = "<textarea name='message'>" +  textarea_content + "</textarea>"

    password_label = "<label>Password</label>"
    password_input = "<input type=password/>"
    textarea = "<textarea name='message'>" + textarea_content + "</textarea>"

    vpassword_label = "<label>Verify Password</label>"
    vpassword_input = "<input type=verify_password/>"
    textarea = "<textarea name='message'>" + textarea_content + "</textarea>"

    email_label = "<label>Email (optional)</label>"
    email_input = "<input type=email/>"
    textarea = "<textarea name='message'>" + textarea_content + "</textarea>"


    submit = "<input type='submit'/>"

    form = ("<form>" +
            user_label + user_input + "<br>" +
            password_label + password_input + "<br>"  +
            vpassword_label + vpassword_input + "<br>" +
            email_label + email_input + "<br>" +
            submit + "</form>")

    header ="<h1>Signup</h1>"

    return header + form

class MainHandler(webapp2.RequestHandler):
    def get(self):
        content = build_page("")
        self.response.write(content)

    def post(self):
        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
