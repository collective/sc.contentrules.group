# -*- coding:utf-8 -*-
from setuptools import setup, find_packages
import os

version = open(os.path.join("sc", "contentrules",
                            "group", "version.txt")).read().strip()

setup(name='sc.contentrules.group',
      version=version,
      description="Plone content rule to create a group based on a content",
      long_description=(open("README.txt").read() + "\n" +
                        open(os.path.join("docs", "HISTORY.txt")).read()),
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='contentrules action plone group',
      author='Simples Consultoria',
      author_email='products@simplesconsultoria.com.br',
      url='http://www.simplesconsultoria.com.br',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['sc', 'sc.contentrules'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.stringinterp',
      ],
      extras_require={
        'test': ['plone.app.testing'],
        },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
