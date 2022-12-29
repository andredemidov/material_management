import unittest
from domain.repositories.related_material_repository import RelatedMaterialRepository
from domain.entities.material_related import MaterialRelated


class TestRelatedMaterialRepository(unittest.TestCase):

    pass


class FakePostDataAdapter:

    @staticmethod
    def create_related_material(related_materials_for_create):
        return True
