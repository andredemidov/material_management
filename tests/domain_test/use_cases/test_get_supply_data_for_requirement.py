import unittest
from datetime import datetime
from src.domain.use_cases.get_supply_data_for_requirement import GetSupplyDataForRequirements
from src.domain.entities.material_requirement import MaterialRequirement
from src.domain.entities.material_related import MaterialRelated
from src.domain.entities.material_supply import MaterialSupply
from src.domain.entities.material_notification import MaterialNotification
from src.domain.entities.material_order import MaterialOrder
from src.domain.repositories.repository import Repository


class TestGetSupplyDataForRequirements(unittest.TestCase):

    def setUp(self) -> None:
        self.supply = MaterialSupply(
            code='forvalidation',
            amount=2000,
            root_id='forvalidation',
            root_name='forvalidation',
            max_date=datetime.now(),
            issued=0,
            supplied=2000,
            name='forvalidation'
        )
        self.rest_supply = MaterialSupply(
            code='forvalidation',
            amount=100,
            root_id='forvalidation',
            root_name='forvalidation',
            max_date=datetime.now(),
            issued=0,
            supplied=80,
            name='forvalidation'
        )
        self.free_supply = MaterialSupply(
            code='forvalidation',
            amount=5,
            root_id='forvalidation',
            root_name='forvalidation',
            max_date=datetime.now(),
            issued=0,
            supplied=5,
            name='forvalidation'
        )
        self.notification = MaterialNotification(
            code='forvalidation',
            shipped=15,
            delivery_date=datetime.now(),
            shipping_date=datetime.now(),
        )
        self.notification.shipped_available = 15
        self.order = MaterialOrder(
            code='forvalidation',
            contractor_id='forvalidation',
            moving=1000,
            delivered=1000,
        )
        requirements = list()
        for i in range(50, 330, 5):
            related_materials = [
                MaterialRelated(
                    host='forvalidation',
                    code='forvalidation',
                    supply=self.supply,
                    rest_supply=[self.rest_supply],
                    free_supply=self.free_supply,
                    notification=self.notification,
                    order=self.order,
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
            )

            requirements.append(requirement)
        self.stub_repository = Repository(requirements)

    def test_execute_sample_data_right_return(self):
        # arrange
        stub_repository = self.stub_repository
        requirements = stub_repository.list()

        # act
        GetSupplyDataForRequirements(stub_repository).execute()

        # assert
        supply_amount = list(set(map(lambda x: x.new_supply_amount, requirements)))
        self.assertEqual(len(supply_amount), 1)
        self.assertEqual(supply_amount[0], self.supply.amount)

        supplied = list(set(map(lambda x: x.new_supplied, requirements)))
        self.assertEqual(len(supplied), 1)
        self.assertEqual(supplied[0], self.supply.supplied)

        issued = list(set(map(lambda x: x.issued, requirements)))
        self.assertEqual(len(issued), 1)
        self.assertEqual(issued[0], self.supply.issued)

        max_date = list(set(map(lambda x: x.new_max_date, requirements)))
        self.assertEqual(len(max_date), 1)
        self.assertEqual(max_date[0], self.supply.max_date)

        rest_total_available = list(set(map(lambda x: x.new_rest_total_available, requirements)))
        self.assertEqual(len(rest_total_available), 1)
        self.assertEqual(rest_total_available[0], self.rest_supply.total_available)

        free_total_available = list(set(map(lambda x: x.new_free_total_available, requirements)))
        self.assertEqual(len(free_total_available), 1)
        self.assertEqual(free_total_available[0], self.free_supply.total_available)

        total_moving = list(set(map(lambda x: x.new_total_moving, requirements)))
        self.assertEqual(len(total_moving), 1)
        self.assertEqual(total_moving[0], self.order.moving)

        total_delivered = list(set(map(lambda x: x.new_total_delivered, requirements)))
        self.assertEqual(len(total_delivered), 1)
        self.assertEqual(total_delivered[0], self.order.delivered)

        shipped_total_available = list(set(map(lambda x: x.new_shipped_total_available, requirements)))
        self.assertEqual(len(shipped_total_available), 1)
        self.assertEqual(shipped_total_available[0], self.notification.shipped)

        sum_available = sum(list(map(lambda x: x.new_available, requirements)))
        self.assertEqual(sum_available, self.supply.total_available)

        sum_rest_available = sum(list(map(lambda x: x.new_rest_available, requirements)))
        self.assertEqual(sum_rest_available, self.rest_supply.total_available)

        sum_free_available = sum(list(map(lambda x: x.new_free_available, requirements)))
        self.assertEqual(sum_free_available, self.free_supply.total_available)

        sum_moving = sum(list(map(lambda x: x.new_moving, requirements)))
        self.assertEqual(sum_moving, self.order.moving)

        sum_delivered = sum(list(map(lambda x: x.new_delivered, requirements)))
        self.assertEqual(sum_delivered, self.order.delivered)

        sum_shipped_available = sum(list(map(lambda x: x.new_shipped_available, requirements)))
        self.assertEqual(sum_shipped_available, self.notification.shipped)

        for requirement in requirements:
            target_sum = requirement.total_available + requirement.new_moving
            self.assertLessEqual(target_sum, requirement.amount)

    def test_execute_sample_data_mounted_first(self):
        # arrange
        stub_repository = self.stub_repository
        requirements = stub_repository.list()

        # act
        FakeGetSupplyDataForRequirements(stub_repository).execute()

        # assert
        for requirement in requirements:
            self.assertLessEqual(requirement.new_moving, requirement.remainder_for_moving_from_mounted)
            target_sum = requirement.total_available + requirement.new_moving
            self.assertLessEqual(target_sum, requirement.amount)


class FakeGetSupplyDataForRequirements(GetSupplyDataForRequirements):

    def _get_supply_data(self, requirements):
        pass
