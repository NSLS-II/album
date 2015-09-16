from flask import Flask, render_template, request
from dataportal import DataBroker as db
from dataportal.broker.simple_broker import get_table
from bokeh_plot import plot_table_by_time

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
    
    table = get_table(h, fill=True)
    bokeh_kw = plot_table_by_time(table)
    return render_template('run_show.html', uid=uid, fields=fields,
                           **bokeh_kw)


def run(debug=False):
    app.run(debug=debug)


if __name__ == '__main__':
    run(debug=True)
