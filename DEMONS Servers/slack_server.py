# Copyright []
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
### BEGIN NODE INFO
[info]
name = Slack Server
version = 0.0
description = Send message/figures to Slack  

[startup]
cmdline = %PYTHON% %FILE%
timeout = 20

[shutdown]
message = 987654321
timeout = 20
### END NODE INFO
"""


from labrad.server import LabradServer, setting
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.internet import reactor, defer
import labrad.units as units
from labrad.types import Value
from labrad.errors import Error
import sys
import requests
from slack import WebClient


class SlackClient(LabradServer):
    name = "Slack Server"    # Will be labrad name of server


    def getBot(self, c):
    	return c['SlackBot']

    @setting(10, 'Connect Bot',
    		 token=['s: Token of bot'],
    		 returns=['s: Connected bot info'])
    def connect_bot(self, c, token=''):
    	if 'SlackBot' in c:
    		del c['SlackBot']

    	bot_client = WebClient(token=token)
    	c['SlackBot'] = bot_client
    	return bot_client.auth_test().data['user']


    @setting(11, 'Send message',
    		 channel=['s: Channel destination'],
    		 message=['s: Message to send'])
    def send_message(self, c, channel, message):
    	bot = self.getBot(c)
    	response = bot.chat_postMessage(channel=channel, text=message)

    def sleep(self,secs):
        """Asynchronous compatible sleep command. Sleeps for given time in seconds, but allows
        other operations to be done elsewhere while paused."""
        d = defer.Deferred()
        reactor.callLater(secs,d.callback,'Sleeping')
        return d

__server__ = SlackServer()
  
if __name__ == '__main__':
    from labrad import util
    util.runServer(__server__)