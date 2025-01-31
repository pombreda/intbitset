# -*- coding: utf-8 -*-
#
# This file is part of intbitset
# Copyright (C) CERN and others
#
# SPDX-License-Indetifier: LGPL-3.0-or-later
#
# intbitset is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# intbitset is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with intbitset; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
#
# In applying this licence, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""C-based extension implementing fast integer bit sets."""

import os
import re
import platform

from setuptools import Extension
from setuptools import setup


# Get the version string. Cannot be done with import!
with open(os.path.join('intbitset', 'intbitset_version.py'), 'rt') as f:
    version = re.search(
        '__version__\s*=\s*"(?P<version>.*)"\n',
        f.read()
    ).group('version')

extra_compile_args=['-O3', '-mtune=native']

# If we let default optimizer, we'll get instructions that are valid only for similar arch as build machine
# hence the wheel will generate invalid instruction exception for more ancient machine generation
# for x86, we choose core2 as minimal target as per commit b15854c6382d
if platform.machine() in ['i386', 'x86_64']:
    extra_compile_args.append('-march=core2')
                  
# For debug -> extra_compile_args.append('-ftree-vectorizer-verbose=2')
extra_compile_args = []
setup(
    name='intbitset',
    version=version,
    url='http://github.com/inveniosoftware/intbitset/',
    license='LGPL-3.0-or-later',
    author='Invenio collaboration',
    author_email='info@inveniosoftware.org',
    description=__doc__,
    long_description=open('README.rst').read(),
    package_dir={'': 'intbitset'},
    py_modules=['intbitset_helper', 'intbitset_version'],
    ext_modules=[
        Extension("intbitset",
                  ["intbitset/intbitset.c", "intbitset/intbitset_impl.c"],
                  extra_compile_args=extra_compile_args
                  )
    ],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        "six",
    ],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Cython',
        'Programming Language :: C',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        # 'Development Status :: 5 - Production/Stable',
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
)
