#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example Bowtie App.
"""

from bowtie.control import Nouislider
from bowtie.visual import Plotly
from bowtie import command
from bowtie import Pager
from bowtie import cache

import numpy as np
from numpy import random as rng
import plotlywrapper as pw


pager = Pager()
sigma = Nouislider(caption='Sigma', start=0., minimum=0.1, maximum=50.)
mainplot = Plotly()


def initialize():
    cache.save('data', [0.] * 100)


def upgraph():
    data = cache.load('data')
    value = float(sigma.get())
    data.pop(0)
    data.append(value * rng.randn() + data[-1])
    mainplot.do_all(pw.line(data).to_json())
    cache.save('data', data)


def walk():
    pager.notify()


@command
def construct():
    from bowtie import Layout
    layout = Layout(debug=False)
    layout.add_sidebar(sigma)
    layout.add(mainplot)
    layout.load(initialize)
    layout.schedule(0.1, walk)
    layout.respond(pager, upgraph)

    layout.build()
