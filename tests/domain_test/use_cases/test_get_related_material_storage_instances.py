import unittest
from domain.entities import MaterialStorage, MaterialRelated, MaterialRequirement
from domain.repositories import RequirementRepository, StoragesRepository
from domain.use_cases.get_related_material_storage_instances import GetRelatedMaterialStorageInstances


class TestGetRelatedMaterialStorageInstances(unittest.TestCase):

    def test_execute(self):
        # arrange
        stub_storages = [
            MaterialStorage(
                storage_id='s1',
                code='0123456789',
                root_name='forvalidation',
                root_id='forvalidation',
                reserved=0
            ),
            MaterialStorage(
                storage_id='s2',
                code='0123456789',
                root_name='forvalidation',
                root_id='forvalidation',
                reserved=0
            ),
            MaterialStorage(
                storage_id='s3',
                code='0123456789',
                root_name='forvalidation',
                root_id='forvalidation',
                reserved=0
            )
        ]
        mock_related_materials = [
            MaterialRelated('forvalidation', '0123456789'),
            MaterialRelated('forvalidation', '0123401234'),
        ]
        stub_requirement = MaterialRequirement(
            item_id='forvalidation',
            name='forvalidation',
            main_code='forvalidation',
            construction_object='forvalidation',
            level_4='forvalidation',
            axes='forvalidation',
            priority='forvalidation',
            amount=0,
            plan_date=0,
            mounted=0,
            mounted_spool=0,
            related_materials=mock_related_materials,
            construction='forvalidation',
            construction_subobject='forvalidation',
            level_3='forvalidation',
            project_section='forvalidation',
            weld=0,
            onsite_storage_ids=['s1']
        )
        stub_repository = RequirementRepository(
            get_data_adapter=None,
            post_data_adapter=None,
            root=None,
            entries=[stub_requirement]
        )
        stub_storages_repository = StoragesRepository(
            get_data_adapter=None,
            root=None,
            entries=stub_storages
        )
        # act
        GetRelatedMaterialStorageInstances(stub_repository, stub_storages_repository).execute()

        # assert
        all_storages = stub_storages_repository.get()
        all_storages_codes = [s.code for s in all_storages]
        for requirement in stub_repository.get():
            for related_material in requirement.related_materials:
                # check if all storages distributed in related material
                if related_material.code in all_storages_codes:
                    total_storages = len(related_material.onsite_storage) + len(related_material.remote_storage)
                    count = all_storages_codes.count(related_material.code)
                    self.assertEqual(count, total_storages)

                # check if all onsite storages putted into related material
                onsite_storages = list(
                    filter(lambda x: x.code == related_material.code and x.storage_id in requirement.onsite_storage_ids,
                           all_storages))
                self.assertEqual(len(onsite_storages), len(related_material.onsite_storage))

                if related_material.onsite_storage:
                    # check if onsite storages in related material match to onsite storage id in requirement
                    onsite_storages_ids = [s.storage_id for s in related_material.onsite_storage]
                    for storage_id in onsite_storages_ids:
                        self.assertIn(storage_id, requirement.onsite_storage_ids)
                    # check if storages codes match to related material code
                    storages_codes = [s.code for s in related_material.onsite_storage]
                    self.assertEqual(len(set(storages_codes)), 1)
                    self.assertEqual(storages_codes[0], related_material.code)
