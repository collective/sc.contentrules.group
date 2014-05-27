# -*- coding:utf-8 -*-
from OFS.SimpleItem import SimpleItem
from plone.app.contentrules.browser.formhelper import AddForm
from plone.app.contentrules.browser.formhelper import EditForm
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleElementData
from plone.stringinterp.interfaces import IStringInterpolator
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from sc.contentrules.group import MessageFactory as _
from sc.contentrules.group.interfaces import ICreateGroupAction
from ZODB.POSException import ConflictError
from zope.component import adapts
from zope.formlib import form
from zope.interface import implements, Interface


class GroupAction(SimpleItem):
    """The actual persistent implementation of the action element.
    """
    implements(ICreateGroupAction, IRuleElementData)

    groupid = ''
    grouptitle = ''
    roles = ''
    element = "sc.contentrules.group.CreateGroup"

    @property
    def summary(self):
        roles = ', '.join(self.roles)
        return _(u"Create an user group ${groupid} with roles ${roles}",
                 mapping=dict(roles=roles, groupid=self.groupid))


class GroupActionExecutor(object):
    """The executor for this action.
    """
    implements(IExecutable)
    adapts(Interface, ICreateGroupAction, Interface)

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
        # User interpolator to process principal information
        # This way it's possible to set Group_${title}
        # and receive a Group_ContentTitle
        groupid = interpolator(groupid).strip()
        if gt.getGroupById(groupid):
            self.error(obj,
                       _(u'An user group with the same id already exists.'))
            return False
        grouptitle = self.element.grouptitle
        grouptitle = interpolator(grouptitle).strip()

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
            message = _(u"Unable to create user group with id "
                        u"${groupid}: ${error}",
                        mapping={'groupid': groupid, 'error': error})
            IStatusMessage(request).addStatusMessage(message, type="error")


class GroupAddForm(AddForm):
    """An add form for create group action.
    """
    form_fields = form.FormFields(ICreateGroupAction)
    label = _(u"Add an action that creates an user group")
    description = _(u"Create an user group as a result of this action")

    def create(self, data):
        a = GroupAction()
        form.applyChanges(a, self.form_fields, data)
        return a


class GroupEditForm(EditForm):
    """An edit form for create group rule action.
    """
    form_fields = form.FormFields(ICreateGroupAction)
    label = _(u"Edit an action that creates an user group")
    description = _(u"Create an user group as a result of this action")
