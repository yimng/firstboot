#!/usr/bin/python2.2

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
continueButton = (_("_Reread license"))
shutdownButton = (_("_Shut down"))
