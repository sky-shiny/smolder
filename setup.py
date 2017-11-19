#!/usr/bin/env python

import os
import sys

from setuptools import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

PACKAGES = [
    'smolder',
]

REQUIRES = [
    'argh >= 0.26.1',
    'decorator >= 3.4.0',
    'dpath >= 1.2-70',
    'ecdsa >= 0.11',
    'Jinja2 >= 2.7.3',
    'MarkupSafe >= 0.23',
    'requests >= 2.5.0',
    'retry >= 0.4.2',
    'retrying >= 1.3.3',
    'six >= 1.8.0',
    'jsonpickle >= 0.9.2',
    'PyYAML >= 3.11',
    'Yapsy >= 1.11.23',
    'validictory >= 1.0.0',
    'nose >= 1.3.7',
    'httpretty == 0.8.10',
    'ldap3'
]

with open('README.md', 'r') as f:
    README = f.read()

setup(
    name='smolder',
    version='0.6.0.0',
    description='Json wrapper around requests for simple smoke testing.',
    long_description=README,
    author='Max Cameron',
    author_email='maxwell.cameron@johngaltsystems.com',
    url='http://sky-shiny.github.io/smolder/',
    packages=PACKAGES,
    package_data={'': ['LICENSE', '*.yapsy-plugin']},
    package_dir={'smolder': 'charcoal'},
    scripts=['smolder'],
    include_package_data=True,
    install_requires=REQUIRES,
    license='BSD License',
    zip_safe=False,
    classifiers=(
    ), requires=['requests', 'httpretty', 'nose', 'jsonpickle', 'argh', 'decorator', 'dpath',
                 'ecdsa', 'Jinja2', 'MarkupSafe', 'requests', 'retry', 'retrying', 'six',
                 'jsonpickle', 'PyYAML', 'Yapsy', 'validictory', 'nose', 'httpretty','ldap3']
)
