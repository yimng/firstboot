#!/usr/bin/python2

from distutils.core import setup
from glob import *

setup(name='firstboot', version='1.110',
      description='Post-installation configuration utility',
      author='Martin Gracik', author_email='mgracik@redhat.com',
      url='http://fedoraproject.org/wiki/FirstBoot',
      data_files=[('/usr/sbin', ['progs/firstboot']),
                  ('/usr/share/firstboot/themes/default', glob('themes/default/*.png')),
                  ('/usr/share/firstboot/modules', glob('modules/*.py')),
                  ('/lib/systemd/system', glob('systemd/*.service')),
                 ],
      packages=['firstboot'])
