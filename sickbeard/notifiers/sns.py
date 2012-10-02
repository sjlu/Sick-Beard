# Author: Marvin Pinto <me@marvinp.ca>
# Author: Dennis Lutter <lad1337@gmail.com>
# Author: Aaron Bieber <deftly@gmail.com>
# URL: http://code.google.com/p/sickbeard/
#
# This file is part of Sick Beard.
#
# Sick Beard is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Sick Beard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sick Beard.  If not, see <http://www.gnu.org/licenses/>.

import urllib, urllib2

import sickbeard

from sickbeard import logger
from sickbeard.common import notifyStrings, NOTIFY_SNATCH, NOTIFY_DOWNLOAD
from sickbeard.exceptions import ex

API_URL = "http://sns.burst-dev.com/api/notification"

class SnsNotifier:

    def test_notify(self, userKey=None):
        return self._sendSns("This is a test notification from SickBeard", 'Notification Test')

    def _sendSns(self, msg, sub, userKey = None):
        """
        Places a POST to the SNS service.

        msg: The message to send.
        sub: The title to send.
        """
        
        if not userKey:
            userKey = sickbeard.SNS_USERKEY

        # build up the URL and parameters
        msg = msg.strip()
        curUrl = API_URL

        data = urllib.urlencode({
            'key': userKey,
            'subject': sub,
            'message': msg.encode('utf-8'),
		})

        # send the request to SNS
        try:
            req = urllib2.Request(curUrl)
            handle = urllib2.urlopen(req, data)
            handle.close()
        except urllib2.URLError, e:
            logger.log("Failed to send to SNS. " + ex(e), logger.ERROR)
            return False

        logger.log("SNS message successfully sent.", logger.DEBUG)
        return True

    def notify_snatch(self, ep_name, title=notifyStrings[NOTIFY_SNATCH]):
        if sickbeard.SNS_NOTIFY_ONSNATCH:
            self._notifySns(title, ep_name)

    def notify_download(self, ep_name, title=notifyStrings[NOTIFY_DOWNLOAD]):
        if sickbeard.SNS_NOTIFY_ONDOWNLOAD:
            self._notifySns(title, ep_name)

    def _notifySns(self, subject, message, userKey=None):
        """
        Sends a notification to the SNS service.

        subject: The subject
        message: The message string to send
        """

        if not sickbeard.USE_SNS:
            logger.log("SNS is not enabled, skipping.", logger.DEBUG)
            return False

        if not userKey:
            userKey = sickbeard.SNS_USERKEY

        self._sendSns(message, subject)
        return True

notifier = SnsNotifier