#!/usr/bin/python3

#
# lxd-term
#
# Copyright (c) 2020 Daniel Dean <dd@danieldean.uk>.
#
# Licensed under The MIT License a copy of which you should have
# received. If not, see:
#
# http://opensource.org/licenses/MIT
#

from pylxd import Client
import web

ENDPOINT = 'mini-server:8443'
CONTAINER = 'test'
SHELL = 'bash'  # Must match shell of the container.
ENVIRONMENT = {
    "HOME": "/root",
    "TERM": "xterm",
    "USER": "root"
}

urls = (
    '/', 'Index'
)

render = web.template.render('templates/')
app = web.application(urls, globals())


def get_ws_uri():
    client = Client(endpoint='https://' + ENDPOINT, cert=('client.crt', 'client.key'), verify=False)
    container = client.containers.get(CONTAINER)
    return 'wss://' + ENDPOINT + container.raw_interactive_execute([SHELL], ENVIRONMENT)['ws']


class Index:
    def GET(self):
        return render.index(get_ws_uri())


if __name__ == "__main__":
    app.run()
