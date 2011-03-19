import subprocess
import os
import tarfile
import zipfile
import sys
import re

def verify_file(file_location,expected_verification_code,method='md5sum'):
    verification_output = subprocess.check_output(['/usr/bin/%s' % (method,), file_location]).strip()
    (verification_code, filename) = re.split(r'\s+', verification_output,2)
    if verification_code != expected_verification_code:
        print "Alert the military, the %s checksum does not match what it should!" % (filename,)
        print "Expected: %s" % (expected_verification_code,)
        print "Seen    : %s" % (verification_code,)
        sys.exit(0)

def download_file(url,file_location):
    statement = '/usr/bin/wget -q -O "%s" "%s"' % (file_location,url)
    subprocess.call(statement,shell=True)

def download_and_install(package_name, package_to_info_hash):
    info = package_to_info_hash[package_name]

    if os.path.exists(info['successfully_installed']):
        return True

    downloads_directory = info['downloads_directory']
    bin_directory = info['bin_directory']
    python_location = info['python_location']
    primary_directory = info['primary_directory']
    download_method = info.get('download_method', 'wget')

    decompressed_directory = '%s%s' % (downloads_directory,package_name,)

    if not os.path.exists(info['successfully_installed']):
        if download_method == 'hg':
           subprocess.call('/usr/bin/hg clone "%s" "%s"' % (info['download_url'], info['successfully_installed'],),shell=True)
        elif not os.path.exists(decompressed_directory):
            download_location = '%s%s' % (downloads_directory, info['download_filename'],)

            if not os.path.exists(download_location):
                download_file(info['download_url'],download_location)

            if not os.path.exists(download_location):
                print "%s not found" % (download_location,)
                sys.exit(0)
            else:
                if info.get('verification_method'):
                    verify_file(download_location, info['verification_code'], info['verification_method'])

            if not os.path.exists(decompressed_directory):
                if info['decompression_method'] == 'tgz':
                    tar = tarfile.open(download_location)
                    tar.extractall(path=downloads_directory)
                    directory = tar.getnames()[0]
                    tar.close()
                    source_directory = '%s%s' % (downloads_directory, directory,)
                    os.symlink(source_directory, decompressed_directory) 
                if info['decompression_method'] == 'zip' and package_name == 'appengine':
                    output_directory = "%s/../" % (info['primary_directory'],)
                    subprocess.call('/usr/bin/unzip -q "%s" -d "%s"' % (download_location, output_directory,),shell=True)
                    print "%s | %s" % (output_directory, '%s/.google_appengine' % (primary_directory,))
                    # os.symlink(output_directory, '%s/.google_appengine' % (primary_directory,))


        if package_name == 'appengine':
            pass
        elif info['shared']:
            symlink_directory = "%s/%s" % (info['primary_directory'],package_name)
            source_directory = info['successfully_installed']
            if package_name == 'django-nonrel':
                source_directory = "%s/django" % (source_directory,)
                symlink_directory = "%s/django" % (info['primary_directory'],)
            if package_name == 'djangotoolbox':
                source_directory = "%s/djangotoolbox" % (source_directory,)
            if not os.path.exists(symlink_directory):
                print "%s -> %s" % (source_directory, symlink_directory)
                os.symlink(source_directory, symlink_directory) 
        elif package_name == 'python':
            os.chdir(decompressed_directory)
            configure_statement = '/bin/bash configure --prefix="%s"' % (bin_directory,)
            print configure_statement
            subprocess.call(configure_statement,shell=True)

            make_statement = '/usr/bin/make'
            print make_statement
            subprocess.call(make_statement,shell=True)

            make_install_statement = '/usr/bin/make install'
            print make_install_statement
            subprocess.call(make_install_statement,shell=True)

            os.chdir(primary_directory)
        else:
            os.chdir(decompressed_directory)
            install_statement = '%s %s/setup.py install' % (python_location, decompressed_directory,)
            print install_statement
            subprocess.call(install_statement,shell=True)
            os.chdir(primary_directory)

