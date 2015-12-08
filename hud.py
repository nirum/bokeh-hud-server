"""
Bokeh HUD server

"""

__version__ = '0.0.1'

from time import strftime
from functools import wraps
from bokeh.io import output_server
from bokeh.session import Session
from bokeh.plotting import figure, show, cursession
import numpy as np

def login(password, username='nirum'):
    session = Session()
    session.login(username, password)


def publish(func):
    """
    Decorator for publishing a figure

    """
    @wraps(func)
    def wrapper(*args, **kwargs):

        name = kwargs.pop('name', strftime('%I:%M:%S %h %d %Y'))
        width = kwargs.pop('w', 800)
        height = kwargs.pop('h', 500)

        output_server(name)
        p = figure(plot_width=width, plot_height=height)
        p = func(p, *args, **kwargs)
        show(p)

    return wrapper


@publish
def line(p, x, y=None, **kwargs):

    if y is None:
        y = x
        x = np.arange(y.size)

    p.line(x, y, **kwargs)


def stream(name, width=800, height=500):
    """
    Broken
    """

    output_server(name)

    p = figure(plot_width=width, plot_height=height)
    p.line([1,2,3], [4,5,6], name='ex_line')

    renderer = p.select({'name': 'ex_line'})
    ds = renderer[0].data_source

    while True:

        x, y = yield

        ds.data['x'] = x
        ds.data['y'] = y

        cursession().store_objects(ds)

        show(p)
