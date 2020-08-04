# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2011 NovaReto GmbH

import grok
from fanstatic import Library, Resource
from uvc.widgets import double
from uvc.widgets import masked_input

library = Library('ukh.adhoc', 'static')
css = Resource(library, 'main.css')

stepcss = Resource(library, 'step.css', bottom=True)
meinedatencss = Resource(library, 'meinedaten.css', bottom=True)
kontocss = Resource(library, 'konto.css', bottom=True)
step1js = Resource(library, 'step1.js', depends=[double], bottom=True)
ah_css = Resource(library, 'ukh_ah.css')
badge_css = Resource(library, 'badge.css')
lb_badge_css = Resource(library, 'lb_badge.css', bottom=True)
