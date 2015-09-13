from flask import Flask, render_template, request
from dataportal import DataBroker as db


app = Flask(__name__)


@app.route('/')
def home():
    return 'This is album.'


@app.route('/runs')
def run_index():
    # /runs?page=1 loads db[-10:0], /runs?page=2 loads db[-20:-10], etc.
    # RUNS_PER_PAGE could be configurable too, but probably best to do that
    # as a session variable so it's persistent. This is good for now.
    RUNS_PER_PAGE = 10
    print(request.args)
    page = int(request.args.get('page', 1))
    start, stop = -RUNS_PER_PAGE * page, -RUNS_PER_PAGE * (page - 1)
    headers = db[start:stop]
    return render_template('run_index.html', headers=headers, page=page,
                           start=start, stop=stop)


@app.route('/run/<uid>')
def run_show(uid):
    h = db[uid]
    fields = []
    for descriptor in h['descriptors']:
        for field in descriptor['data_keys']:
            fields.append(field)
    return render_template('run_show.html', uid=uid, fields=fields)


if __name__ == '__main__':
    app.run(debug=True)
