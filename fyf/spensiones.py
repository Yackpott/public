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

URL = 'http://www.spensiones.cl/safpstats/stats/rentabilidad/getRentab.php?tiprent=FP'



@app.route('/')
def index():
    anos = ['2011','2012','2013','2014','2015','2016']
    mes = ['01','02','03','04','05','06','07','08','09','10','11','12']
    for an in anos:
        for me in mes:
            params = dict()
            params['aaaa'] = an
            params['mm'] = me
            params['btn'] = 'Buscar'
            session = requests.Session()
            responsePOST = session.post(URL, data=params)
            with open(an + "-" + me, "w") as f:
                f.write(responsePOST.text)
    return ''

if __name__ == '__main__':
    app.run(port=8080)
