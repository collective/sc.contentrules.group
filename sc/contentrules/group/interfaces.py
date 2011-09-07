# -*- coding: utf-8 -*-
import re
from zope.interface import implements
from zope.interface import Interface
from zope import schema

from sc.contentrules.group import MessageFactory as _


class IGroupAction(Interface):
    """An action used to create a group
    """

    groupid = schema.TextLine(title=_(u"Group Id"),
                      description=_(u"Please inform the id for the group \
                                      that will be created by this action."),
                      required=True,
                )

    grouptitle = schema.TextLine(title=_(u"Group title"),
                          description=_(u"A title for the new group."),
                          required=False,
                )

    roles = schema.Set(title=_(u"Roles"),
                         description=_(u"Roles to be assigned to this group."),
                         required=True,
                         value_type=schema.Choice(
                                    vocabulary='plone.app.vocabularies.Roles',
                ))
