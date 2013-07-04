# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>


class MissingParametersError(ValueError):

    def __init__(self, missing_parameters):
        ValueError.__init__(self, "Missing parameters: %s" % ','.join(missing_parameters))


class InvalidParametersError(ValueError):

    def __init__(self, invalid_parameters):
        ValueError.__init__(self, "Invalid parameters: %s" % ','.join(invalid_parameters))


class ElementAlreadyExistsError(ValueError):

    def __init__(self, element, *args):
        ValueError.__init__(self, "%s %s already exists" % (element, ' '.join(args)))


class ElementNotExistsError(LookupError):

    def __init__(self, element, **kwargs):
        err = []
        for key, value in kwargs.iteritems():
            err.append('%s=%s' % (key, value))
        LookupError.__init__(self, "%s with %s not exists" % (element, ' '.join(err)))


class ElementCreationError(IOError):

    def __init__(self, element, error):
        message = "error while creating %s: %s" % (element, unicode(error))
        IOError.__init__(self, message)


class ElementEditionError(IOError):

    def __init__(self, element, error):
        message = "error while editing %s: %s" % (element, unicode(error))
        IOError.__init__(self, message)


class ElementDeletionError(IOError):

    def __init__(self, element, error):
        message = "error while deleting %s: %s" % (element, unicode(error))
        IOError.__init__(self, message)