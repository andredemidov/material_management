import unittest
from random import choice
from datetime import datetime
from src.domain.use_cases.get_supply_data_for_requirement import GetSupplyDataForRequirements
from src.domain.entities.material_requirement import MaterialRequirement
from src.domain.entities.material_related import MaterialRelated
from src.domain.entities.material_supply import MaterialSupply
from src.domain.entities.material_notification import MaterialNotification
from src.domain.entities.material_order import MaterialOrder
from src.domain.entities.material_storage import MaterialStorage
from src.domain.repositories.requirement_repository import RequirementRepository


class TestGetSupplyDataForRequirements(unittest.TestCase):

    def setUp(self) -> None:
        self.supply = MaterialSupply(
            code='0000000000',
            amount=2000,
            root_id='forvalidation',
            root_name='forvalidation',
            max_date=datetime.now(),
            issued=0,
            supplied=2000,
            name='forvalidation'
        )
        self.rest_supplies = [
            MaterialSupply(
                code='0000000000',
                amount=100,
                root_id='forvalidation',
                root_name='forvalidation',
                max_date=datetime.now(),
                issued=0,
                supplied=80,
                name='forvalidation'
            ),
            MaterialSupply(
                code='0000000000',
                amount=20,
                root_id='forvalidation',
                root_name='forvalidation',
                max_date=datetime.now(),
                issued=0,
                supplied=5,
                name='forvalidation'
            )
            ]
        self.free_supply = MaterialSupply(
            code='0000000000',
            amount=5,
            root_id='forvalidation',
            root_name='forvalidation',
            max_date=datetime.now(),
            issued=0,
            supplied=5,
            name='forvalidation'
        )
        self.notification = MaterialNotification(
            code='0000000000',
            shipped=15,
            max_delivery_date=datetime.now(),
            max_shipping_date=datetime.now(),
        )
        self.notification.shipped_available = 15
        self.order = MaterialOrder(
            code='0000000000',
            contractor_id='forvalidation',
            moving=1000,
            delivered=1000,
        )
        self.onsite_storages = [
            MaterialStorage(
                code='00000000',
                reserved=50,
                storage_id='1',
                storage_name='onsite',
                name='forvalidation',
                root_name='forvalidation',
                root_id='forvalidation',
            ),
            MaterialStorage(
                code='00000000',
                reserved=100,
                storage_id='1',
                storage_name='onsite',
                name='forvalidation',
                root_name='forvalidation',
                root_id='forvalidation',
            ),
        ]
        self.remote_storages = [
            MaterialStorage(
                code='00000000',
                reserved=200,
                storage_id='2',
                storage_name='remote',
                name='forvalidation',
                root_name='forvalidation',
                root_id='forvalidation',
            ),
            MaterialStorage(
                code='00000000',
                reserved=250,
                storage_id='3',
                storage_name='remote',
                name='forvalidation',
                root_name='forvalidation',
                root_id='forvalidation',
            ),
        ]

        requirements = list()
        for i in range(50, 330, 5):
            related_materials = [
                MaterialRelated(
                    host='forvalidation',
                    self_name='forvalidation',
                    code='0000000000',
                    supply=self.supply,
                    rest_supply=self.rest_supplies,
                    free_supply=self.free_supply,
                    onsite_storage=self.onsite_storages,
                    remote_storage=self.remote_storages,
                    notification=self.notification,
                    order=self.order,
                    name_valid=choice([True, False]),
                    delete=False,
                ),
            ]
            requirement = MaterialRequirement(
                item_id='forvalidation',
                name='forvalidation',
                main_code='forvalidation',
                construction_object='forvalidation',
                level_4='forvalidation',
                axes='forvalidation',
                priority='forvalidation',
                amount=i,
                plan_date=0,
                mounted=i * 0.2 if i % 10 == 0 else i,
                mounted_spool=i * 0.1,
                related_materials=related_materials,
                construction='forvalidation',
                construction_subobject='forvalidation',
                level_3='forvalidation',
                project_section='forvalidation',
                weld=0,
            )

            requirements.append(requirement)
        self.stub_repository = RequirementRepository(
            get_data_adapter=None,
            post_data_adapter=None,
            root=None,
            entries=requirements
        )

    def test_execute_sample_data_right_return(self):
        # arrange
        stub_repository = self.stub_repository
        requirements = stub_repository.get()

        # act
        GetSupplyDataForRequirements(stub_repository).execute()

        # assert
        total_attrs = [
            ('new_supply_amount', self.supply.amount),
            ('new_supplied', self.supply.supplied),
            ('new_issued', self.supply.issued),
            ('new_rest_total_available', sum([rest.total_available for rest in self.rest_supplies])),
            ('new_free_total_available', self.free_supply.total_available),
            ('new_total_moving', self.order.moving),
            ('new_total_delivered', self.order.delivered),
            ('new_shipped_total_available', self.notification.shipped),
        ]
        sum_attrs = [
            ('new_available', self.supply.total_available),
            ('new_rest_available', sum([rest.total_available for rest in self.rest_supplies])),
            ('new_free_available', self.free_supply.total_available),
            ('new_moving', self.order.moving),
            ('new_delivered', self.order.delivered),
            ('new_shipped_available', self.notification.shipped),
            ('new_onsite_storage_available', sum([store.reserved for store in self.onsite_storages])),
            ('new_remote_storage_available', sum([store.reserved for store in self.remote_storages])),
        ]
        for attr, value in total_attrs:
            values = sorted(list(set(map(lambda x: getattr(x, attr), requirements))))
            self.assertEqual(values[0], 0)
            self.assertEqual(values[-1], value, attr)

        for attr, target_value in sum_attrs:
            value = sum(list(map(lambda x: getattr(x, attr), requirements)))
            self.assertEqual(value, target_value, attr)

        # max_dates = list(set(map(lambda x: x.new_max_date, requirements)))
        # self.assertEqual(max_dates[0], 0)
        # self.assertEqual(max_dates[-1], self.supply.max_date)

        for requirement in requirements:
            target_sum = requirement.total_available + requirement.new_moving
            self.assertLessEqual(target_sum, requirement.amount)

            related_materials = list(filter(lambda x: x.valid(), requirement.related_materials))
            available = sum([x.available for x in related_materials]) if related_materials else 0
            self.assertEqual(available, requirement.new_available)

    def test_execute_sample_data_mounted_first(self):
        # arrange
        stub_repository = self.stub_repository
        requirements = stub_repository.get()

        # act
        FakeGetSupplyDataForRequirements(stub_repository).execute()

        # assert
        for requirement in requirements:
            self.assertLessEqual(requirement.new_moving, requirement.remainder_for_moving_from_mounted)
            target_sum = requirement.total_available + requirement.new_moving
            self.assertLessEqual(target_sum, requirement.amount)

    def test_execute_only_valid_false_distribution_regardless_to_validity(self):
        # arrange
        stub_repository = self.stub_repository
        requirements = stub_repository.get()

        # act
        GetSupplyDataForRequirements(stub_repository, only_valid=False).execute()

        # assert
        for requirement in requirements:
            related_materials = list(filter(lambda x: not x.delete, requirement.related_materials))
            target_sum = sum([x.supply.amount for x in related_materials]) if related_materials else 0
            self.assertEqual(target_sum, requirement.new_supply_amount)

    def test_execute_sum_storage_is_equal_available(self):
        # arrange
        stub_repository = self.stub_repository
        requirements = stub_repository.get()

        # act
        GetSupplyDataForRequirements(stub_repository).execute()

        # assert
        for requirement in requirements:
            related_materials = list(filter(lambda x: not x.delete, requirement.related_materials))
            onsite_storage_available = sum(
                [x.onsite_storage_available for x in related_materials]) if related_materials else 0
            self.assertEqual(onsite_storage_available, requirement.new_onsite_storage_available)

            remote_storage_available = sum(
                [x.remote_storage_available for x in related_materials]) if related_materials else 0
            self.assertEqual(remote_storage_available, requirement.new_remote_storage_available)

            storage_sum = requirement.new_onsite_storage_available + requirement.new_remote_storage_available
            self.assertLessEqual(storage_sum, requirement.total_available)


class FakeGetSupplyDataForRequirements(GetSupplyDataForRequirements):

    def _get_supply_data(self, requirements):
        pass
