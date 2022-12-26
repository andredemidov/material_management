from typing import List
from domain.entities import MaterialRequirement, MaterialOrder


class GetRelatedMaterialOrderInstances:

    def __init__(self, requirement_repository, material_order_repository):
        self._requirement_repository = requirement_repository
        self._material_order_repository = material_order_repository

    @staticmethod
    def _find_order(requirement: MaterialRequirement, orders_contractors: dict):
        relevant_orders = orders_contractors.get(requirement.contractor_id)
        if relevant_orders:
            for related_material in requirement.related_materials:
                related_material.order = relevant_orders.get(related_material.code)

    @staticmethod
    def _get_orders_dict(orders: List[MaterialOrder]) -> dict:
        """возвращает словарь со структурой {'contractor_id' : {'code': order}}"""
        # По аналогии с SQL в таблицу orders добавил индексы contractor и code.
        # При поиске это позволяет сначала быстро искать нужного contractor, а потом быстро найти нужный заказ по коду
        orders_contractors = {}
        for order in orders:
            if order.contractor_id not in orders_contractors:
                orders_contractors[order.contractor_id] = {}
            orders_contractors[order.contractor_id][order.code] = order
        return orders_contractors

    def execute(self):
        orders = self._material_order_repository.get()
        orders_contractors = self._get_orders_dict(orders)
        requirements_with_contractor = tuple(filter(lambda x: x.contractor_id, self._requirement_repository.get()))

        for requirement in requirements_with_contractor:
            self._find_order(requirement, orders_contractors)
        print('get orders instances complete')
