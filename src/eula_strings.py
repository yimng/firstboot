## eula_strings.py 
##
## Copyright (C) 2003 Red Hat, Inc.
## Copyright (C) 2003 Brent Fox <bfox@redhat.com>
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

##
## I18N
## 
from rhpl.translate import _, N_
import rhpl.translate as translate
translate.textdomain ("firstboot")

moduleName = (_("License Agreement"))
yes = (_("_Yes, I agree to the License Agreement"))
no = (_("N_o, I do not agree"))
dlgMsg = (_("Do you want to reread or reconsider the License Agreement?"))
dlgMsg2 = (_("Do you want to reread or reconsider the Licence Agreement?  If not, please shut down the computer and remove this product from your system. "))
continueButton = (_("_Reread license"))
shutdownButton = (_("_Shut down"))
