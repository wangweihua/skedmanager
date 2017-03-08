#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='skedmanager',
    version='0.1.0',
    description="Sked Manager",
    long_description=readme + '\n\n' + history,
    author="Weihua Wang",
    author_email='whwang@shao.ac.cn',
    url='https://github.com/wangweihua/skedmanager',
    packages=[
        'skedmanager',
    ],
    package_dir={'skedmanager':
                 'skedmanager'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='skedmanager',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
