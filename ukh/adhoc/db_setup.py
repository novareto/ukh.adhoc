# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import os
import grok

from z3c.saconfig import EngineFactory, GloballyScopedSession
from sqlalchemy import Table, MetaData
from zope.app.appsetup.product import getProductConfiguration

config = getProductConfiguration('database')
DSN = config['dsn']
SCHEMA = config.get('schema', 'EDUCUSADAT')

engine_factory = EngineFactory(DSN, echo=False)
scoped_session = GloballyScopedSession()

grok.global_utility(engine_factory, direct=True)
grok.global_utility(scoped_session, direct=True)


engine = engine_factory()
metadata = MetaData(bind=engine)
if os.environ['ADHOC_TEST'] == "True":
    c1unf1aa = None 
    c1prs1aa = None
    avika1aa = None
    zczve1aa = None
    zckto1aa = None

else:
    c1unf1aa = Table(config['c1unf1aa'], metadata, schema=SCHEMA, autoload=True, autoload_with=engine)
    c1prs1aa = Table(config['c1prs1aa'], metadata, schema=SCHEMA, autoload=True, autoload_with=engine)
    avika1aa = Table(config['avika1aa'], metadata, schema=SCHEMA, autoload=True, autoload_with=engine)
    zczve1aa = Table(config['zczve1aa'], metadata, schema=SCHEMA, autoload=True, autoload_with=engine)
    zckto1aa = Table(config['zckto1aa'], metadata, schema=SCHEMA, autoload=True, autoload_with=engine)

