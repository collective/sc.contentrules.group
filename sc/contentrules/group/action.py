# -*- coding:utf-8 -*-
from plone.contentrules.rule.interfaces import IExecutable, IRuleElementData
from zope.interface import implements, Interface
from zope.component import adapts
from zope.formlib import form

from plone.stringinterp.interfaces import IStringInterpolator

from OFS.SimpleItem import SimpleItem
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from ZODB.POSException import ConflictError

from plone.app.contentrules.browser.formhelper import AddForm, EditForm

from sc.contentrules.group.interfaces import IGroupAction

from sc.contentrules.group import MessageFactory as _


class GroupAction(SimpleItem):
    """The actual persistent implementation of the action element.
    """
    implements(IGroupAction, IRuleElementData)

    groupid = ''
    grouptitle = ''
    roles = ''
    element = "sc.contentrules.group.CreateGroup"

    @property
    def summary(self):
        roles = ', '.join(self.roles)
        return _(u"Create a group ${groupid} with roles ${roles}",
                 mapping=dict(role=[roles], groupid=self.groupid))


class GroupActionExecutor(object):
    """The executor for this action.
    """
    implements(IExecutable)
    adapts(Interface, IGroupAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        obj = self.event.object
        gt = getToolByName(self.context, 'portal_groups', None)
        interpolator = IStringInterpolator(obj)
        if gt is None:
            return False

        roles = list(self.element.roles)
        groupid = self.element.groupid
        #User interpolator to process principal information
        # This way it's possible to set Group_${title}
        # and receive a Group_ContentTitle
        groupid = interpolator(groupid).strip()
        if gt.getGroupById(groupid):
            self.error(obj, _(u'A group with the same id already exists.'))
            return False
        grouptitle = self.element.grouptitle

        try:
            gt.addGroup(groupid, title=grouptitle, roles=roles)
        except ConflictError, e:
            raise e
        except Exception, e:
            self.error(obj, str(e))
            return False

        return True

    def error(self, obj, error):
        request = getattr(self.context, 'REQUEST', None)
        if request is not None:
            groupid = self.element.groupid
            message = _(u"Unable to create group with id ${groupid}: ${error}",
                          mapping={'groupid': groupid, 'error': error})
            IStatusMessage(request).addStatusMessage(message, type="error")


class GroupAddForm(AddForm):
    """An add form for group action.
    """
    form_fields = form.FormFields(IGroupAction)
    label = _(u"Add an action to create a group")
    description = _(u"An action that creates a group based on \
                      an object.")
    form_name = _(u"Configure element")

    def create(self, data):
        a = GroupAction()
        form.applyChanges(a, self.form_fields, data)
        return a


class GroupEditForm(EditForm):
    """An edit form for group rule action.
    """
    form_fields = form.FormFields(IGroupAction)
    label = _(u"Edit an action to create a group")
    description = _(u"An action that creates a group based on \
                      an object.")
    form_name = _(u"Configure element")
