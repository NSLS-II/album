import flask
from flask import Flask, render_template, request
from dataportal import DataBroker as db
from dataportal.broker.simple_broker import get_table
import bokeh
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.templates import RESOURCES
from bokeh.util.string import encode_utf8
from bokeh.charts import TimeSeries
from bokeh.io import vplot, hplot
import numpy as np
import time as ttime
import pandas as pd
from datetime import datetime


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
def run_show(*args, **kwargs):
    if args:
        print('args = %s' % args)
    print('kwargs = %s' % kwargs)
    args = flask.request.args
    print('args = %s' % args)
    uid = kwargs['uid']
    h = db[uid]
    fields = []
    for descriptor in h['descriptors']:
        for field in descriptor['data_keys']:
            fields.append(field)
    
    table = get_table(h, fill=False)
    # now = ttime.time()
    # data = {'time': [datetime.fromtimestamp(now + _) for _ in range(100)],
    #         'd1': np.sin(np.arange(0, 1, .01)),
    #         'd2': np.cos(np.arange(0, 1, .01))}
    # table = pd.DataFrame(data, index=range(100))
    plots = []
    for k, v in table.items():
        if k == 'time':
            continue
        df = pd.DataFrame(v.values, index=table['time'], columns=[k])
        df = df.dropna()
        x_range = plots[0].x_range if plots else None
        fig = figure(title=k, x_axis_type='datetime', x_range=x_range)
        fig.line(df.index, df[k], line_width=2)
        fig.circle(df.index, df[k], fill_color='white', size=8)
        plots.append(fig)
    
    ncols = int(np.ceil(np.sqrt(len(plots))))
    nrows = int(np.ceil(len(plots) / ncols))
    rows = [hplot(*plots[row*ncols:(row+1)*ncols]) for row in range(nrows)]
    plot = vplot(*rows)
    print('plot = %s' % plot)
    script, div = components(plot)
    
    plot_resources = RESOURCES.render(
        js_raw=INLINE.js_raw,
        css_raw=INLINE.css_raw,
        js_files=INLINE.js_files,
        css_files=INLINE.css_files,
    )
    return render_template('run_show.html', uid=uid, fields=fields,
                           plot_div=div,
                           plot_resources=plot_resources,
                           plot_script=script,
                           bokeh_version=bokeh.__version__)

if __name__ == '__main__':
    app.run(debug=True)
