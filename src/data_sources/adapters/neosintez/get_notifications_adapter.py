from typing import List
from datetime import datetime
from domain.entities import Root, MaterialNotification
from data_sources.gateways.neosintez import MakeSearchRequests

from .abstract_adapter import AbstractAdapter


class GetNotificationsAdapter(AbstractAdapter):

    def __init__(self, session):
        super().__init__(session)
        self._notification_data = list()
        self._notifications = list()

    def _get_all_notification_data(self, root_id):
        print('Get notifications is called.')
        payload = {
            "Filters": [
                {
                    "Type": 4,
                    "Value": root_id
                },
                {
                    "Type": 5,
                    "Value": self.notification_class_id
                }
            ],
        }
        payloads = [
            {
                'route': '',
                'request_body': payload,
            }
        ]
        results = MakeSearchRequests.execute(payloads, self._session, 'post')
        for result in results:
            if result['status'] != 200:
                message = f"one or more search requests have status not equal 200. {result['data']}"
                raise RuntimeError(message)
            self._notification_data.extend(result['data']['Result'])
        print('Response of notifications is got', len(self._notification_data))

    def _get_notification_data(self, root_id, date: datetime):
        print('Get notifications is called.', end=' ')
        date_string = datetime.strftime(date, '%Y-%m-%dT%H:%M:%S')
        payload = {
            "Filters": [
                {
                    "Type": 4,
                    "Value": root_id
                },
                {
                    "Type": 5,
                    "Value": self.notification_class_id
                }
            ],
            "Conditions": [
                {
                    "Type": 1,
                    "Direction": 0,
                    "Logic": 0,
                    "Attribute": f'{self.actual_attribute_id}',
                    "Operator": 4,
                    "Value": date_string
                },
            ]
        }
        payloads = [
            {
                'route': '',
                'request_body': payload,
            }
        ]
        results = MakeSearchRequests.execute(payloads, self._session, 'post')
        for result in results:
            if result['status'] != 200:
                message = f"one or more search requests have status not equal 200. {result['data']}"
                raise RuntimeError(message)
            self._notification_data.extend(result['data']['Result'])
        print('Response of notifications is got', len(self._notification_data))

    def _init_orders(self, item):

        attributes = item['Object']['Attributes']
        code = self.get_value(attributes, self.code_attribute_id)
        shipped = self.get_value(attributes, self.shipped_attribute_id, attribute_type='int')
        unit = self.get_value(attributes, self.unit_attribute_id)
        delivery_date = self.get_value(attributes, self.delivery_date_attribute_id)
        shipping_date = self.get_value(attributes, self.shipping_date_attribute_id)

        next_notification = MaterialNotification(
            code=code,
            shipped=shipped,
            delivery_date=delivery_date,
            shipping_date=shipping_date,
            unit=unit,
        )
        if next_notification in self._notifications:
            index = self._notifications.index(next_notification)
            exist_notification = self._notifications[index]
            exist_notification.shipped += next_notification.shipped

            self._notifications[index] = exist_notification
        else:
            self._notifications.append(next_notification)

    def execute(self, root: Root, date: datetime = None) -> List[MaterialNotification]:
        if date:
            self._get_notification_data(root.root_id, date)
        else:
            self._get_all_notification_data(root.root_id)

        for item in self._notification_data:
            self._init_orders(item)
        return self._notifications
