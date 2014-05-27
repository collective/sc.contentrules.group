**************************************
Content Rules: User group actions
**************************************

.. contents:: Content
   :depth: 2

Overview
--------

**Content Rules: User group actions** (sc.contentrules.group) package provides
content rule actions to create or remove an user group.

This package is tested with Travis CI:

.. image:: https://secure.travis-ci.org/simplesconsultoria/sc.contentrules.group.png
    :alt: Travis CI badge
    :target: http://travis-ci.org/simplesconsultoria/sc.contentrules.group

.. image:: https://coveralls.io/repos/simplesconsultoria/sc.contentrules.group/badge.png?branch=master
    :alt: Coveralls badge
    :target: https://coveralls.io/r/simplesconsultoria/sc.contentrules.group

.. image:: https://pypip.in/d/sc.contentrules.group/badge.png
    :target: https://pypi.python.org/pypi/sc.contentrules.group/
    :alt: Downloads

Use case
---------

A college with descentralized content management and groups dedicated to research. Each group should manage its own content.

In their portal they want to host areas for each research group they sponsor.
All those areas will be under the folder /research/. A research group called
"Environmental Studies" will have an area at /research/environmental-studies.

Every time a new research group is added under /research/ they need to create at
least two user groups:

* Editors: Group of users responsible for publishing content and managing
  this area.

* Members: Group of users with access to this area.

Also, every time a research group is removed from /research/ they want to remove
existing user groups related to it.

Installation
------------

To enable this product,on a buildout based installation:

1. Edit your buildout.cfg and add ``sc.contentrules.group``
   to the list of eggs to install ::

    [buildout]
    ...
    eggs =
        sc.contentrules.group

After updating the configuration you need to run the ''bin/buildout'',
which will take care of updating your system.

Actions
---------

This package provides two content rules actions, one to create a new user
group, other to remove an existing user group.

Create User Group
^^^^^^^^^^^^^^^^^^^

Used to create a new user group this action have three options:

Group Id
    Unique name for the newly created group. You are allowed to use ${title} in
    here to dinamically generate the id for the group. i.e.: If this field have
    a value of **${title} Editors** and the action is being executed for a
    folder with title "Environmental Studies", Group Id will be
    "Environmental Studies Editors"

Group Title
    Friendly name for the newly created group. You are allowed to use ${title}
    in here to dinamically create the id for the group. i.e.: If this field
    have a value of **Editors for Research Group: ${title}** and the action is
    being executed for a folder with title "Environmental Studies", Group Title
    will be "Editors for Research Group: Environmental Studies"

Roles
    Global roles for newly created group. Roles selected here will be effective
    in the whole portal.

.. note:: In order to apply a local role -- set a role for the newly created
          group only in the object that triggered the content rule -- you need
          to have the **sc.contentrules.localrole** package installed and use
          the package's provided action.


Remove User Group
^^^^^^^^^^^^^^^^^^^

Used to remove an existing user group this action have just one option:

Group Id
    Id of the group to be removed. You are allowed to use ${title} in
    here to dinamically generate the id for the group. i.e.: If this field have
    a value of **${title} Editors** and the action is being executed for a
    folder with title "Environmental Studies", Group Id will be
    "Environmental Studies Editors"
