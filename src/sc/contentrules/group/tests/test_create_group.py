# -*- coding:utf-8 -*-
from OFS.interfaces import IObjectManager
from plone.app.contentrules.rule import Rule
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleAction
from Products.CMFCore.utils import getToolByName
from sc.contentrules.group.actions.create import GroupAction
from sc.contentrules.group.actions.create import GroupEditForm
from sc.contentrules.group.testing import INTEGRATION_TESTING
from zope.component import getUtility, getMultiAdapter
from zope.component.interfaces import IObjectEvent
from zope.interface import implements

import unittest2 as unittest


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
        # setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']
        self.gt = self.portal.portal_groups
        self.gt.addGroup('Fav Customer', title='Our Fav Customer', roles=())

    def testRegistered(self):
        element = getUtility(IRuleAction,
                             name='sc.contentrules.group.CreateGroup')
        self.assertEquals('sc.contentrules.group.CreateGroup',
                          element.addview)
        self.assertEquals('edit', element.editview)
        self.assertEquals(IObjectManager, element.for_)
        self.assertEquals(IObjectEvent, element.event)

    def testInvokeAddView(self):
        element = getUtility(IRuleAction,
                             name='sc.contentrules.group.CreateGroup')
        storage = getUtility(IRuleStorage)
        storage[u'foo'] = Rule()
        rule = self.portal.restrictedTraverse('++rule++foo')

        adding = getMultiAdapter((rule, self.portal.REQUEST), name='+action')
        addview = getMultiAdapter((adding, self.portal.REQUEST),
                                  name=element.addview)

        addview.createAndAdd(data={'groupid': 'Users',
                                   'grouptitle': 'Users of this portal',
                                   'roles': set(['Reader', ])})

        e = rule.actions[0]
        self.failUnless(isinstance(e, GroupAction))
        self.assertEquals('Users', e.groupid)
        self.assertEquals('Users of this portal', e.grouptitle)
        self.assertEquals(set(['Reader', ]), e.roles)

    def testInvokeEditView(self):
        element = getUtility(IRuleAction,
                             name='sc.contentrules.group.CreateGroup')
        e = GroupAction()
        editview = getMultiAdapter((e, self.folder.REQUEST),
                                   name=element.editview)
        self.failUnless(isinstance(editview, GroupEditForm))

    def testExecute(self):
        e = GroupAction()
        e.groupid = 'New Group'
        e.grouptitle = 'Newly Created Group'
        e.roles = set(['Member', ])

        ex = getMultiAdapter((self.portal, e, DummyEvent(self.folder)),
                             IExecutable)
        self.assertEquals(True, ex())
        group = self.gt.getGroupById(e.groupid)
        self.failUnless(group)

    def testExecuteInterp(self):
        # Setup scenario
        self.portal.invokeFactory('Folder', 'customer', title='Customer')
        folder = self.portal['customer']
        e = GroupAction()
        e.groupid = '${title}'
        e.grouptitle = 'Group of Contributors for folder ${title}'
        e.roles = set(['Contributor', ])

        ex = getMultiAdapter((self.portal, e, DummyEvent(folder)),
                             IExecutable)
        self.assertEquals(True, ex())
        group = self.gt.getGroupById(folder.Title())
        self.failUnless(group)
        self.failUnless(group.getGroupId() == folder.Title())
        grouptitle = 'Group of Contributors for folder %s' % folder.Title()
        self.failUnless(group.getGroupTitleOrName() == grouptitle)

    def testActionSummary(self):
        e = GroupAction()
        e.groupid = '${title}'
        e.grouptitle = 'Group of Contributors for folder ${title}'
        e.roles = set(['Contributor', ])
        summary = u'Create an user group ${groupid} with roles ${roles}'
        self.assertEquals(summary, e.summary)

    def testExecuteWithoutGroupManagementPlugin(self):
        ''' No group management plugins enabled '''
        from Products.PlonePAS.interfaces.group import IGroupManagement
        # Disable group management plugins
        acl_users = getToolByName(self.portal, 'acl_users')
        acl_users.plugins.deactivatePlugin(IGroupManagement,
                                           'source_groups')
        # Execute action
        e = GroupAction()
        e.groupid = 'New Group'
        e.grouptitle = 'Newly Created Group'
        e.roles = set(['Member', ])

        ex = getMultiAdapter((self.portal, e, DummyEvent(self.folder)),
                             IExecutable)
        self.assertEquals(False, ex())

    def testExecuteWithoutGroupTool(self):
        ''' Test what happens if portal_groups is not available '''
        # Remove portal_tool
        self.portal._delOb('portal_groups')

        # Execute action
        e = GroupAction()
        e.groupid = 'New Group'
        e.grouptitle = 'Newly Created Group'
        e.roles = set(['Member', ])

        ex = getMultiAdapter((self.portal, e, DummyEvent(self.folder)),
                             IExecutable)
        self.assertEquals(False, ex())

    def testExecuteWithError(self):
        ''' Already a group with the same id '''
        e = GroupAction()
        e.groupid = 'Fav Customer'
        e.grouptitle = 'Our Fav Customer'
        e.roles = set(['Member', ])

        ex = getMultiAdapter((self.portal, e, DummyEvent(self.folder)),
                             IExecutable)

        self.assertEquals(False, ex())


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
