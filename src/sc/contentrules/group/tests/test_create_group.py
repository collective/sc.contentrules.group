# -*- coding: utf-8 -*-
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
from zope.component import getMultiAdapter
from zope.component import getUtility
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
        element = getUtility(
            IRuleAction, name='sc.contentrules.group.CreateGroup')
        self.assertEqual(
            'sc.contentrules.group.CreateGroup', element.addview)
        self.assertEqual('edit', element.editview)
        self.assertEqual(IObjectManager, element.for_)
        self.assertEqual(IObjectEvent, element.event)

    def testInvokeAddView(self):
        element = getUtility(
            IRuleAction, name='sc.contentrules.group.CreateGroup')
        storage = getUtility(IRuleStorage)
        storage[u'foo'] = Rule()
        rule = self.portal.restrictedTraverse('++rule++foo')

        adding = getMultiAdapter((rule, self.portal.REQUEST), name='+action')
        addview = getMultiAdapter(
            (adding, self.portal.REQUEST), name=element.addview)

        addview.createAndAdd(data={'groupid': 'Users',
                                   'grouptitle': 'Users of this portal',
                                   'roles': set(['Reader', ])})

        e = rule.actions[0]
        self.assertTrue(isinstance(e, GroupAction))
        self.assertEqual('Users', e.groupid)
        self.assertEqual('Users of this portal', e.grouptitle)
        self.assertEqual(set(['Reader', ]), e.roles)

    def testInvokeEditView(self):
        element = getUtility(
            IRuleAction, name='sc.contentrules.group.CreateGroup')
        e = GroupAction()
        editview = getMultiAdapter(
            (e, self.folder.REQUEST), name=element.editview)
        self.assertTrue(isinstance(editview, GroupEditForm))

    def testExecute(self):
        e = GroupAction()
        e.groupid = 'New Group'
        e.grouptitle = 'Newly Created Group'
        e.roles = set(['Member', ])

        ex = getMultiAdapter(
            (self.portal, e, DummyEvent(self.folder)), IExecutable)
        self.assertEqual(True, ex())
        group = self.gt.getGroupById(e.groupid)
        self.assertTrue(group)

    def testExecuteInterp(self):
        # Setup scenario
        self.portal.invokeFactory('Folder', 'customer', title='Customer')
        folder = self.portal['customer']
        e = GroupAction()
        e.groupid = '${title}'
        e.grouptitle = 'Group of Contributors for folder ${title}'
        e.roles = set(['Contributor', ])

        ex = getMultiAdapter(
            (self.portal, e, DummyEvent(folder)), IExecutable)
        self.assertEqual(True, ex())
        group = self.gt.getGroupById(folder.Title())
        self.assertTrue(group)
        self.assertEqual(group.getGroupId(), folder.Title())
        grouptitle = 'Group of Contributors for folder %s' % folder.Title()
        self.assertEqual(group.getGroupTitleOrName(), grouptitle)

    def testActionSummary(self):
        e = GroupAction()
        e.groupid = '${title}'
        e.grouptitle = 'Group of Contributors for folder ${title}'
        e.roles = set(['Contributor', ])
        summary = u'Create an user group ${groupid} with roles ${roles}'
        self.assertEqual(summary, e.summary)

    def testExecuteWithoutGroupManagementPlugin(self):
        ''' No group management plugins enabled '''
        from Products.PlonePAS.interfaces.group import IGroupManagement
        # Disable group management plugins
        acl_users = getToolByName(self.portal, 'acl_users')
        acl_users.plugins.deactivatePlugin(IGroupManagement, 'source_groups')
        # Execute action
        e = GroupAction()
        e.groupid = 'New Group'
        e.grouptitle = 'Newly Created Group'
        e.roles = set(['Member', ])

        ex = getMultiAdapter(
            (self.portal, e, DummyEvent(self.folder)), IExecutable)
        self.assertEqual(False, ex())

    def testExecuteWithoutGroupTool(self):
        ''' Test what happens if portal_groups is not available '''
        # Remove portal_tool
        self.portal._delOb('portal_groups')

        # Execute action
        e = GroupAction()
        e.groupid = 'New Group'
        e.grouptitle = 'Newly Created Group'
        e.roles = set(['Member', ])

        ex = getMultiAdapter(
            (self.portal, e, DummyEvent(self.folder)), IExecutable)
        self.assertFalse(ex())

    def testExecuteWithError(self):
        ''' Already a group with the same id '''
        e = GroupAction()
        e.groupid = 'Fav Customer'
        e.grouptitle = 'Our Fav Customer'
        e.roles = set(['Member', ])

        ex = getMultiAdapter(
            (self.portal, e, DummyEvent(self.folder)), IExecutable)

        self.assertFalse(ex())
