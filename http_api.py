#
# skaer media streamer
# Copyright (c) 2019 Emil Penchev
#
# Project page:
#   http://skaermedia.org
#
# licensed under GNU GPL version 3 (or later)
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
#


import os
import apps
import cherrypy


class ServerApi(object):
    """ Server REST API. """

    @cherrypy.expose('apps')
    @cherrypy.tools.allow(methods=['GET'])
    @cherrypy.tools.json_out()
    def get_apps(self):
        """ Return a list with information about all loaded media apps
            (name, description ..)

        """
        return [app.info for app in apps.all()]


