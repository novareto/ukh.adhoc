# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok
import zope.component

import uvcsite.plugins
from ukh.adhoc.interfaces import IUKHAdHocApp
from ukh.adhoc.auth import UserAuthenticatorPlugin
from zope.pluggableauth import PluggableAuthentication
from zope.pluggableauth.interfaces import IAuthenticatorPlugin
from grokcore.registries import create_components_registry
from zope.authentication.interfaces import IAuthentication


adhocRegistry = create_components_registry(
    name="ukhadhocRegistry",
    bases=(zope.component.globalSiteManager,)
)


def setup_pau(PAU):
    PAU.authenticatorPlugins = ("users",)
    PAU.credentialsPlugins = (
        "ukh_cookies",
        "Zope Realm Basic-Auth",
        "No Challenge if Authenticated",
    )


class UKHAdHocApp(grok.Application, grok.Container):
    grok.implements(IUKHAdHocApp)

    grok.local_utility(
        PluggableAuthentication,
        IAuthentication,
        public=True,
        setup=setup_pau
    )

    grok.local_utility(
        UserAuthenticatorPlugin,
        provides=IAuthenticatorPlugin,
        name="users"
    )

    def getSiteManager(self):
        current = super(UKHAdHocApp, self).getSiteManager()
        if adhocRegistry not in current.__bases__:
            adhocRegistry.__bases__ = tuple([
                x for x in adhocRegistry.__bases__
                if x.__hash__() != zope.component.globalSiteManager.__hash__()
            ])
            current.__bases__ = (adhocRegistry,) + current.__bases__
        else:
            if current.__bases__.index(adhocRegistry) == 1:
                current.__bases__ = current.__bases__[::-1]
        return current
