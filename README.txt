.. contents:: Table of Contents
   :depth: 2

sc.contentrules.group
**********************************

Overview
--------
    **sc.contentrules.group** is a content rules action that creates a new 
    group in a Plone site when executed.

Use case
---------

    In a portal you have an area for Products. This area, */products* will 
    hold folders for each product available.
    
    Everytime a new folder (product) is added in this area we want a new group 
    of users to be created.
    
    This group can be used to give local roles to its users in this context.
    

Requirements
------------

    * Plone 3.3.x and above (http://plone.org/products/plone)
    
    
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

Sponsoring
----------

Development of this product was sponsored by:
    
    * `Simples Consultoria <http://www.simplesconsultoria.com.br/>`_.


Credits
-------

    * Erico Andrei (erico at simplesconsultoria dot com dot br)

