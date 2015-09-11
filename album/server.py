from flask import Flask
from flask import render_template
from dataportal import DataBroker as db


app = Flask(__name__)


@app.route('/')
def index():
    return 'This is album.'


@app.route('/run/<uid>')
def run(uid):
    h = db[uid]
    fields = []
    for descriptor in h.descriptors:
        for field in descriptor.data_keys.keys():
            fields.append(field)
    return render_template('run.html', uid=uid, fields=fields)


if __name__ == '__main__':
        app.run()
