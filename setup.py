import os
from setuptools import setup, find_packages


version = '1.0'

install_requires=[
    'grok',
    'setuptools',
    'uvcsite',
]

tests_require = [
    'z3c.testsetup',
    'webtest',
    'zope.testbrowser',
]


setup(name='ukh.adhoc',
      version=version,
      description="",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ukh'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      extras_require={'test': tests_require},
      entry_points={
         'fanstatic.libraries': [
            'ukh.adhoc = ukh.adhoc.resources:library',
            ],
         'z3c.autoinclude.plugin': 'target=uvcsite', 
      }
      )
