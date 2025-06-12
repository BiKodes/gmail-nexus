"""Setup file."""
from setuptools import setup, find_packages

from nexus.version import __version__
from nexus.utils import read_file

VERSION = __version__
README = read_file('README.rst', package_level=False)
name = 'gmail-nexus'

setup(
    name=name,
    version=VERSION,
    license='MIT',
    description='Gmail Nexus - Python Client',
    long_description=README,
    author='Biko Olianga',
    author_email='bikocodes@gmail.com',
    url='https://github.com/BiKodes/gmail-nexus',
    keywords=['gmail-nexus', 'gmail python client'],
    packages=find_packages(exclude=['tests', ]),
    install_requires=[
        'google-api-python-client',
        'python-dateutil',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.11',
        
    ],
    include_package_data=True,
)
