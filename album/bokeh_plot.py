import bokeh
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.templates import RESOURCES
from bokeh.io import vplot, hplot
import numpy as np
import pandas as pd
from flask import render_template_string

PLOT_RESOURCES = RESOURCES.render(
    js_raw=INLINE.js_raw,
    css_raw=INLINE.css_raw,
    js_files=INLINE.js_files,
    css_files=INLINE.css_files,
)


BOKEH_HTML_TEMPLATE = """  <head>
  <link
    href="http://cdn.pydata.org/bokeh/release/bokeh-{{ bokeh_version }}.min.css"
    rel="stylesheet" type="text/css">
  <script src="http://cdn.pydata.org/bokeh/release/bokeh-{{ bokeh_version }}.min.js">
  {{ plot_resources|indent(4)|safe }}
  {{ plot_script|indent(4)|safe }}
  </head>
  <body>{{ plot_div|indent(4)|safe }}</body>"""

def plot_table_by_time(table):
    plots = []
    for k, v in table.items():
        if k == 'time':
            continue
        df = pd.DataFrame(v.values, index=table['time'], columns=[k])
        df = df.dropna()
        if df[k].values[0].shape:
            # replace with the sum
            df[k] = [np.sum(arr) for arr in df[k]]
        print('k = %s ... df[k][0] = %s' % (k, df[k][0]))
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
    return {'plot_div': div, 'plot_resources': PLOT_RESOURCES,
            'plot_script': script, 'bokeh_version': bokeh.__version__}
