from application.factories.builders.child_root_distribution_builder import ChildRootDistributionBuilder
from application.factories.builders.child_root_deleting_builder import ChildRootDeletingBuilder
from application.factories.builders.child_root_normalizing_builder import ChildRootNormalizingBuilder


class OperateChildRootFactory:

    def __init__(self):
        self._builders = {
            'distribution': ChildRootDistributionBuilder(),
            'deleting': ChildRootDeletingBuilder(),
            'normalization': ChildRootNormalizingBuilder(),
        }

    def create(self, key, **kwargs):
        builder = self._builders.get(key)
        if not builder:
            raise ValueError(key)
        return builder(**kwargs)
