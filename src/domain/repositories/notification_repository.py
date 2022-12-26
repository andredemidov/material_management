from typing import Sequence
from .repository import Repository
from domain.entities import Root, MaterialNotification


class NotificationRepository(Repository):

    def __init__(self, get_data_adapter, root: Root, entries: list = None):
        super().__init__(entries=entries, get_data_adapter=get_data_adapter)
        self._root = root

    @property
    def root_id(self):
        return self._root.root_id

    def _get_from_data_source(self):
        notifications = self._get_data_adapter.get_notifications(self._root)
        self.add(notifications)

    def add(self, entries):
        if isinstance(entries, Sequence) and all(map(lambda x: isinstance(x, MaterialNotification), entries)):
            self._entries.extend(entries)
        elif isinstance(entries, MaterialNotification):
            self._entries.append(entries)
        else:
            raise TypeError('Only instance of MaterialNotification may be added into notifications repository')
