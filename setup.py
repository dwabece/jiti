"""
Build module for timeoff library
"""
from setuptools import setup

REQUIREMENTS = [
    'jira',
    'click'
]

setup(
    name='jiti',
    version='1.0',
    description='',
    python_requires='>3.6',
    url='https://github.com/dwabece/jiti',
    author='dwabece',
    author_email='mjk@c40.pl',
    packages=['jiti'],
    install_requires=REQUIREMENTS,
    scripts=['bin/jiti'],
    zip_safe=True,
)
