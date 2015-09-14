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
    print("Table\n-----\n%s" % table)
    plot = TimeSeries(table, legend=True)
    # for k, v in table.items():
    #     plot.circle(v.index, v)
        
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

colors = {
    'Black': '#000000',
    'Red':   '#FF0000',
    'Green': '#00FF00',
    'Blue':  '#0000FF',
}


def getitem(obj, item, default):
    if item not in obj:
        return default
    else:
        return obj[item]
        
        
@app.route('/run/<uid>/plotter')
def some_plotter(uid):
    """ Very simple embedding of a polynomial chart"""
    # Grab the inputs arguments from the URL
    # This is automated by the button
    args = flask.request.args

    # Get all the form arguments in the url with defaults
    color = colors[getitem(args, 'color', 'Black')]
    _from = int(getitem(args, '_from', 0))
    to = int(getitem(args, 'to', 10))

    # Create a polynomial line graph
    x = list(range(_from, to + 1))
    fig = figure(title="Polynomial")
    fig.line(x, [i ** 2 for i in x], color=color, line_width=2)

    # Configure resources to include BokehJS inline in the document.
    # For more details see:
    #   http://bokeh.pydata.org/en/latest/docs/reference/resources_embedding.html#module-bokeh.resources
    plot_resources = RESOURCES.render(
        js_raw=INLINE.js_raw,
        css_raw=INLINE.css_raw,
        js_files=INLINE.js_files,
        css_files=INLINE.css_files,
    )

    # For more details see:
    #   http://bokeh.pydata.org/en/latest/docs/user_guide/embedding.html#components
    script, div = components(fig, INLINE)
    html = flask.render_template(
        'embed_plot.html',
        plot_script=script, plot_div=div, plot_resources=plot_resources,
        color=color, _from=_from, to=to
    )
    return encode_utf8(html)

if __name__ == '__main__':
    app.run(debug=True)
