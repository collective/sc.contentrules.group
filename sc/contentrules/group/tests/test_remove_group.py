# -*- coding:utf-8 -*-

import unittest2 as unittest

from OFS.interfaces import IObjectManager

from zope.component import getUtility, getMultiAdapter
from zope.component.interfaces import IObjectEvent
from zope.interface import implements

from plone.app.contentrules.rule import Rule
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IRuleAction
from plone.contentrules.rule.interfaces import IExecutable

from sc.contentrules.group.actions.remove import GroupAction
from sc.contentrules.group.actions.remove import GroupEditForm
from sc.contentrules.group.testing import INTEGRATION_TESTING


class DummyEvent(object):
    implements(IObjectEvent)

    def __init__(self, object):
        self.object = object


class TestGroupAction(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        self.folder = self.portal['test-folder']
        self.gt = self.portal.portal_groups
        self.gt.addGroup('Fav Customer', title='Our Fav Customer', roles=())

    def testRegistered(self):
        element = getUtility(IRuleAction,
                             name='sc.contentrules.group.RemoveGroup')
        self.assertEquals('sc.contentrules.group.RemoveGroup',
                          element.addview)
        self.assertEquals('edit', element.editview)
        self.assertEquals(IObjectManager, element.for_)
        self.assertEquals(IObjectEvent, element.event)

    def testInvokeAddView(self):
        element = getUtility(IRuleAction,
                             name='sc.contentrules.group.RemoveGroup')
        storage = getUtility(IRuleStorage)
        storage[u'foo'] = Rule()
        rule = self.portal.restrictedTraverse('++rule++foo')

        adding = getMultiAdapter((rule, self.portal.REQUEST), name='+action')
        addview = getMultiAdapter((adding, self.portal.REQUEST),
                                  name=element.addview)

        addview.createAndAdd(data={'groupid': 'Users'})

        e = rule.actions[0]
        self.failUnless(isinstance(e, GroupAction))
        self.assertEquals('Users', e.groupid)

    def testInvokeEditView(self):
        element = getUtility(IRuleAction,
                             name='sc.contentrules.group.RemoveGroup')
        e = GroupAction()
        editview = getMultiAdapter((e, self.folder.REQUEST),
                                   name=element.editview)
        self.failUnless(isinstance(editview, GroupEditForm))

    def testExecute(self):
        e = GroupAction()
        e.groupid = 'Fav Customer'

        ex = getMultiAdapter((self.portal, e, DummyEvent(self.folder)),
                             IExecutable)
        self.assertEquals(True, ex())
        group = self.gt.getGroupById(e.groupid)
        self.failIf(group)

    def testExecuteInterp(self):
        # Setup scenario
        self.portal.invokeFactory('Folder', 'customer', title='Fav Customer')
        folder = self.portal['customer']
        e = GroupAction()
        e.groupid = '${title}'

        ex = getMultiAdapter((self.portal, e, DummyEvent(folder)),
                             IExecutable)
        self.assertEquals(True, ex())
        group = self.gt.getGroupById(folder.Title())
        self.failIf(group)

    def testExecuteWithError(self):
        e = GroupAction()
        e.groupid = 'Non Existent Group'

        ex = getMultiAdapter((self.portal, e, DummyEvent(self.folder)),
                             IExecutable)

        self.assertEquals(False, ex())


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
