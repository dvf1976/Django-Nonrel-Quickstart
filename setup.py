#!/usr/bin/env python

import md5
import subprocess
import os
import re
import sys
import tarfile

sys.path.append('lib')

from install_utils import download_and_install

primary_directory = os.getcwd()

downloads_directory = '%s/.downloads/' % (primary_directory,)
bin_directory = '%s/../python2.5/' % (primary_directory,)
shared_directory = '%s/../shared/' % (primary_directory,)
python_location = '%sbin/python2.5' % (bin_directory,)
easy_install_location = '%s/bin/easy_install' % (bin_directory,)

package_to_info_hash = {
    'python' : {
        'download_url'          : 'http://www.python.org/ftp/python/2.5.5/Python-2.5.5.tgz',
        'decompression_method'  : 'tgz',
        'verification_method'   : 'md5sum',
        'verification_code'     : 'abc02139ca38f4258e8e372f7da05c88',
        'download_filename'     : 'Python-2.5.5.tgz',
        'successfully_installed': python_location,
    },
    'easy_install' : {
        'download_url'          : 'http://pypi.python.org/packages/source/s/setuptools/setuptools-0.6c11.tar.gz',
        'decompression_method'  : 'tgz',
        'verification_method'   : 'md5sum',
        'verification_code'     : '7df2a529a074f613b509fb44feefe74e',
        'download_filename'     : 'setuptools.tgz',
        'successfully_installed': easy_install_location,
    },
    'django' : {
        'download_url'          : 'http://www.djangoproject.com/download/1.1.3/tarball/',
        'decompression_method'  : 'tgz',
        'verification_method'   : '',
        'verification_code'     : '',
        'download_filename'     : 'Django.tgz',
        'successfully_installed': '%s/lib/python2.5/site-packages/django' % (bin_directory,),
    },
    'appengine' : {
        'download_url'          : 'http://googleappengine.googlecode.com/files/google_appengine_1.4.2.zip',
        'decompression_method'  : 'zip',
        'verification_method'   : 'sha1sum',
        'verification_code'     : '132d50710b1337169981cd78914d36df29aea722',
        'download_filename'     : 'appengine.zip',
        'successfully_installed': '%s/../google_appengine' % (primary_directory,),
        'symlink_location'      : '%s/.google_appengine' % (primary_directory,)
    },
    'django-nonrel' : {
        'download_url'          : 'https://bitbucket.org/wkornewald/django-nonrel',
        'download_method'       : 'hg',
        'successfully_installed': '%s/django-nonrel' % (shared_directory,),
        'source_location'       : '%s/django-nonrel/django' % (shared_directory,),
        'symlink_location'      : '%s/django' % (primary_directory,),
        'shared'                : True,
    },
    'djangoappengine' : {
        'download_url'          : 'https://bitbucket.org/wkornewald/djangoappengine',
        'download_method'       : 'hg',
        'successfully_installed': '%s/djangoappengine' % (shared_directory,),
        'symlink_location'      : '%s/djangoappengine' % (primary_directory,),
        'shared'                : True,
    },
    'djangotoolbox' : {
        'download_url'          : 'https://bitbucket.org/wkornewald/djangotoolbox',
        'download_method'       : 'hg',
        'successfully_installed': '%s/djangotoolbox' % (shared_directory,),
        'source_location'       : '%s/djangotoolbox/djangotoolbox' % (shared_directory,),
        'symlink_location'      : '%s/djangotoolbox' % (primary_directory,),
        'shared'                : True,
    },
    'django-dbindexer' : {
        'download_url'          : 'https://bitbucket.org/wkornewald/django-dbindexer',
        'download_method'       : 'hg',
        'successfully_installed': '%s/django-dbindexer' % (shared_directory,),
        'symlink_location'      : '%s/django-dbindexer' % (primary_directory,),
        'shared'                : True,
    },
}

"""
'django-testapp' : {
    'download_url'          : 'https://bitbucket.org/wkornewald/django-testapp',
    'download_method'       : 'hg',
    'successfully_installed': '%s/django-testapp' % (shared_directory,),
},
"""

for package in package_to_info_hash:
    package_to_info_hash[package]['primary_directory'] = primary_directory
    package_to_info_hash[package]['downloads_directory'] = downloads_directory
    package_to_info_hash[package]['bin_directory'] = bin_directory
    package_to_info_hash[package]['python_location'] = python_location
    package_to_info_hash[package]['shared_directory'] = shared_directory

if not os.path.exists(downloads_directory):
    os.mkdir(downloads_directory)

download_and_install('python', package_to_info_hash)
download_and_install('easy_install', package_to_info_hash)

for module_name in ['simplejson', 'pyyaml','PIL']:
    install_statement = '%s %s' % (easy_install_location, module_name,)
    print install_statement
    subprocess.call(install_statement,shell=True)
    os.chdir(primary_directory)

download_and_install('django', package_to_info_hash)
download_and_install('appengine', package_to_info_hash)

for package_name in ['django-nonrel', 'djangoappengine', 'djangotoolbox', 'django-dbindexer']:
    download_and_install(package_name, package_to_info_hash)

for package in package_to_info_hash:
    if package_to_info_hash[package].has_key('symlink_location'):
        symlink_location = package_to_info_hash[package]['symlink_location']
        source_location = package_to_info_hash[package].get('source_location', package_to_info_hash[package]['successfully_installed'])
        if not os.path.exists(package_to_info_hash[package]['symlink_location']):
            os.symlink(source_location, symlink_location)
        print "%s exists!" % (symlink_location,)

# statement = '/bin/cp %s/data/test_appserver.datastore /tmp/dev_appserver.datastore' % (primary_directory,)
# subprocess.call(statement,shell=True)

