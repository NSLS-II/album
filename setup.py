from __future__ import (absolute_import, division, print_function)


try:
    from setuptools import setup
except ImportError:
    try:
        from setuptools.core import setup
    except ImportError:
        from distutils.core import setup

from distutils.core import setup

import versioneer


setup(
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    name='album',
    author='Brookhaven National Laboratory',
    packages=['album'],
    entry_points={
        'console_scripts': [
            'album = album.server:run']},
    package_data={'album.templates': ['*.html']},
)
