# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:         sfp_phone
# Purpose:      SpiderFoot plug-in for scanning retreived content by other
#               modules (such as sfp_spider) and identifying phone numbers.
#
# Author:      Steve Micallef <steve@binarypool.com>
#
# Created:     19/06/2016
# Copyright:   (c) Steve Micallef 2016
# Licence:     GPL
# -------------------------------------------------------------------------------

import re
import phonenumbers
from sflib import SpiderFoot, SpiderFootPlugin, SpiderFootEvent

class sfp_phone(SpiderFootPlugin):
    """Phone Numbers:Footprint,Investigate:Social::Identify phone numbers in scraped webpages."""

    # Default options
    opts = {}

    results = list()

    def setup(self, sfc, userOpts=dict()):
        self.sf = sfc
        self.results = list()

        for opt in userOpts.keys():
            self.opts[opt] = userOpts[opt]

    # What events is this module interested in for input
    def watchedEvents(self):
        return ["TARGET_WEB_CONTENT", "DOMAIN_WHOIS", "NETBLOCK_WHOIS"]

    # What events this module produces
    # This is to support the end user in selecting modules based on events
    # produced.
    def producedEvents(self):
        return ["PHONE_NUMBER"]

    # Handle events sent to this module
    def handleEvent(self, event):
        if "sfp_spider" in event.module:
            eventSource = event.sourceEvent
        else:
            eventSource = event
        eventName = event.eventType
        srcModuleName = event.module
        eventData = event.data
        hashData = self.sf.hashstring(eventData)

        if hashData in self.results:
            return None
        else:
            self.results.append(hashData)

        self.sf.debug("Received event, " + eventName + ", from " + srcModuleName)

        for match in phonenumbers.PhoneNumberMatcher(eventData, region=None):
            n = phonenumbers.format_number(match.number, 
                                           phonenumbers.PhoneNumberFormat.E164)
            evt = SpiderFootEvent("PHONE_NUMBER", n, self.__name__, eventSource)
            self.notifyListeners(evt)

        return None

# End of sfp_phone class
