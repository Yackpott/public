import flask
import re
import requests

app = flask.Flask(__name__)

html = """
<!DOCTYPE html>
<html>
<head>
    <title></title>
</head>
<body>
<form action="/login" method="post">
<input type="text" name="username">
<input type="password" name="password">
<input type="submit" value="Submit">
</form>
</body>
</html>
"""

URL = 'https://sso.uc.cl/cas/login'

def parser(names, text):
    ret = dict()
    match = re.finditer("<input type=\"hidden\" name=\"([a-zA-Z0-9_]|-)*\" value=\"([a-zA-Z0-9_]|-)*\" />", text)
    for line in match:
        for name in names:
            if line.group(0).find(name) != -1:
                words = line.group(0).split(" ")
                for word in words:
                    if word[0:5] == "value":
                        ret[name] = word[7:-1]
    return ret
            


@app.route('/')
def index():
    return html


@app.route('/login', methods=['POST'])
def recursos_get():
    session = requests.Session()
    names = ['lt','execution', '_eventId']
    username = flask.request.form['username']
    password = flask.request.form['password']
    responseGET = session.get(URL)
    cookies = session.cookies.get_dict()
    params = parser(names,responseGET.text)
    params['username'] = username
    params['password'] = password
    responsePOST = session.post(URL, data = params, cookies=cookies)
    return ""

if __name__ == '__main__':
    app.run(port=8080)
