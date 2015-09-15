import bokeh
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.templates import RESOURCES
from bokeh.io import vplot, hplot
import numpy as np


PLOT_RESOURCES = RESOURCES.render(
    js_raw=INLINE.js_raw,
    css_raw=INLINE.css_raw,
    js_files=INLINE.js_files,
    css_files=INLINE.css_files,
)


def plot_table_by_time(table):
    plots = []
    table = table.set_index('time')
    for col in table:
        s = table[col]
        s.dropna(inplace=True)
        if not np.isscalar(s.values[0]):
            # replace with the sum
            s = s.apply(np.sum)
        x_range = plots[0].x_range if plots else None
        fig = figure(title=col, x_axis_type='datetime', x_range=x_range)
        fig.line(s.index, s, line_width=2)
        fig.circle(s.index, s, fill_color='white', size=8)
        plots.append(fig)

    ncols = int(np.ceil(np.sqrt(len(plots))))
    nrows = int(np.ceil(len(plots) / ncols))
    rows = [hplot(*plots[row*ncols:(row+1)*ncols]) for row in range(nrows)]
    plot = vplot(*rows)
    print('plot = %s' % plot)
    script, div = components(plot)
    return {'plot_div': div, 'plot_resources': PLOT_RESOURCES,
            'plot_script': script, 'bokeh_version': bokeh.__version__}
