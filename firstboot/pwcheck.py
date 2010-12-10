#
# pwcheck.py
#
# Copyright (C) 2010  Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Red Hat Author(s):  Martin Gracik <mgracik@redhat.com>
#

import re
import cracklib

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pwcheck")

import gettext
_ = lambda x: gettext.ldgettext("firstboot", x)


class PwError(Exception):
    pass


class PwRule(object):

    def __init__(self, rule, weight=1, required=False, desc=""):
        if callable(rule):
            # is a func
            self.rule = rule
        else:
            # is a regex
            pattern = re.compile(rule)
            self.rule = lambda x: bool(pattern.search(x))

        if not weight:
            raise PwError("weight must be a non-zero value")

        self.weight = weight
        self.required = required

        self.desc = desc

    @property
    def include(self):
        return self.weight > 0

    @property
    def exclude(self):
        return self.weight < 0

    def check(self, password):
        passed = self.rule(password)

        if ((self.include and self.required and not passed) or
            (self.exclude and self.required and passed)):
            logger.debug("%s: %d", self.desc, 0)
            raise PwError("password does not meet required criteria")

        if ((self.include and passed) or
            (self.exclude and not passed)):
            logger.debug("%s: %d", self.desc, self.weight)
            return self.weight
        else:
            logger.debug("%s: %d", self.desc, 0)
            return 0


class Password(object):

    def cracklib_check(password):
        try:
            cracklib.FascistCheck(password)
        except ValueError:
            return False
        else:
            return True

    RULES = [ PwRule(rule=lambda x: len(x) >= 4, weight=1, required=True,
                     desc="4 characters or more"),
              PwRule(rule=lambda x: len(x) >= 8, weight=1, required=False,
                     desc="8 characters or more"),
              PwRule(rule=lambda x: len(x) >= 12, weight=1, required=False,
                     desc="12 characters or more"),
              PwRule(rule=r"[a-z]+", weight=1, required=False,
                     desc="at least one lowercase character"),
              PwRule(rule=r"[A-Z]+", weight=1, required=False,
                     desc="at least one uppercase character"),
              PwRule(rule=r"[0-9]+", weight=1, required=False,
                     desc="at least one digit"),
              PwRule(rule=r"[^a-zA-Z0-9]+", weight=1, required=False,
                     desc="at least one special character"),
              PwRule(rule=cracklib_check, weight=-2, required=False,
                     desc="cracklib") ]

    MAX_STRENGTH = 7

    STRENGTH_STRINGS = [ _("Very weak"),
                         _("Very weak"),
                         _("Weak"),
                         _("Weak"),
                         _("Fairly strong"),
                         _("Strong"),
                         _("Very strong"),
                         _("Very strong") ]

    def __init__(self, password):
        self.password = password

    @property
    def strength(self):
        strength = 0
        for rule in self.RULES:
            try:
                strength += rule.check(self.password)
            except PwError:
                return 0

        return strength

    @property
    def strength_string(self):
        strength = self.strength

        if strength < 0:
            return self.STRENGTH_STRINGS[0]

        try:
            return self.STRENGTH_STRINGS[strength]
        except IndexError:
            return _("Undefined")

    @property
    def strength_frac(self):
        frac = float(self.strength) / self.MAX_STRENGTH
        if frac > 1:
            frac = 1.0

        return frac

    def __str__(self):
        return "%s" % self.password
