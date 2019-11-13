# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok

from z3c.saconfig import EngineFactory, GloballyScopedSession
from sqlalchemy import Table, MetaData
from zope.app.appsetup.product import getProductConfiguration

config = getProductConfiguration('database')
DSN = config['dsn']

engine_factory = EngineFactory(DSN, echo=False)
scoped_session = GloballyScopedSession()

grok.global_utility(engine_factory, direct=True)
grok.global_utility(scoped_session, direct=True)


engine = engine_factory()
metadata = MetaData(bind=engine)


c1unf1aa = Table(config['c1unf1aa'], metadata, schema="EDUCUSADAT", autoload=True, autoload_with=engine)
c1prs1aa = Table(config['c1prs1aa'], metadata, schema="EDUCUSADAT", autoload=True, autoload_with=engine)
avika1aa = Table(config['avika1aa'], metadata, schema="EDUCUSADAT", autoload=True, autoload_with=engine)
