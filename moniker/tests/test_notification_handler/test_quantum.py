# Copyright 2012 Managed I.T.
#
# Author: Kiall Mac Innes <kiall@managedit.ie>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from nose import SkipTest
from moniker.openstack.common import log as logging
from moniker.tests.test_notification_handler import AddressHandlerTestCase
from moniker.notification_handler import quantum

LOG = logging.getLogger(__name__)


class QuantumFloatingTestCase(AddressHandlerTestCase):
    __test__ = True
    handler_cls = quantum.QuantumFloatingHandler

    def test_floatingip_associate(self):
        event_type = 'floatingip.update.end'
        fixture = self.get_notification_fixture(
            'quantum', event_type + '_associate')

        self.assertIn(event_type, self.handler.get_event_types())

        # Ensure we start with 0 records
        records = self.central_service.get_records(self.admin_context,
                                                   self.domain_id)

        self.assertEqual(0, len(records))

        self.handler.process_notification(event_type, fixture['payload'])

        # Ensure we now have exactly 1 record
        records = self.central_service.get_records(self.admin_context,
                                                   self.domain_id)

        self.assertEqual(len(records), 1)

    def test_floatingip_disassociate(self):
        start_event_type = 'floatingip.update.end'
        start_fixture = self.get_notification_fixture(
            'quantum', start_event_type + '_associate')
        self.handler.process_notification(start_event_type,
                                          start_fixture['payload'])

        event_type = 'floatingip.update.end'
        fixture = self.get_notification_fixture(
            'quantum', event_type + '_disassociate')

        self.assertIn(event_type, self.handler.get_event_types())

        # Ensure we start with at least 1 record
        records = self.central_service.get_records(self.admin_context,
                                                   self.domain_id)

        self.assertGreaterEqual(len(records), 1)

        self.handler.process_notification(event_type, fixture['payload'])

        records = self.central_service.get_records(self.admin_context,
                                                   self.domain_id)

        self.assertEqual(0, len(records))
