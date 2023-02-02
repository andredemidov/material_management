import aiohttp
from datetime import datetime


class AbstractAdapter:

    supply_class_id = 'b0379bb3-cc70-e911-8115-817c3f53a992'
    title_class_id = 'fa758bdc-0683-ec11-911c-005056b6948b'
    requirement_class_id = '35d52d09-0583-ec11-911c-005056b6948b'
    related_material_class_id = 'ceab91fc-5de5-ec11-9130-005056b6948b'
    child_root_class_id = 'fa758bdc-0683-ec11-911c-005056b6948b'
    main_root_class_id = '3aa54908-2283-ec11-911c-005056b6948b'
    free_rest_supplies_folder_class_id = '3b417b9a-bd8e-ec11-911d-005056b6948b'
    cost_center_code_attribute_id = '626370d8-ad8f-ec11-911d-005056b6948b'

    collection_attribute_id = 'bf04c319-5ee5-ec11-9130-005056b6948b'
    title_attribute_id = 'c7ec82e0-f360-e911-8115-817c3f53a992'

    code_attribute_id = 'b1461a5b-0603-eb11-9110-005056b6948b'
    delete_attribute_id = '7d39b7fb-b9eb-ec11-9131-005056b6948b'
    valid_attribute_id = '227eb4c2-af86-ed11-9155-005056b6948b'
    # for supply
    supply_amount_attribute_id = 'cb67f5e8-0315-ea11-910b-005056b6948b'
    date_attribute_id = '30917a41-4356-ec11-911a-005056b6948b'
    issued_attribute_id = '4b1e4c0c-f3ae-ea11-9103-005056b6e70e'
    supplied_attribute_id = '46549c93-f3ae-ea11-9103-005056b6e70e'
    name_attribute_id = '29c13432-f76f-e911-8115-817c3f53a992'
    supply_request_attribute_id = '71dbb6e7-cb70-e911-8115-817c3f53a992'

    # for requirements
    requirement_name_attribute_id = '10548523-4356-ec11-911a-005056b6948b'
    requirement_mark_attribute_id = '2cb21840-d51f-ea11-910b-005056b6948b'
    requirement_amount_attribute_id = 'fdde6847-c6cf-ea11-9110-005056b6948b'
    line_attribute_id = '667bbac0-3f82-ec11-911c-005056b6948b'
    axes_attribute_id = '942ed0ce-23e6-ec11-9130-005056b6948b'
    priority_attribute_id = '52f91c26-0683-ec11-911c-005056b6948b'
    plan_date_attribute_id = '30917a41-4356-ec11-911a-005056b6948b'
    requirement_date_attribute_id = 'c92232db-c6e7-ec11-9130-005056b6948b'
    requirement_issued_attribute_id = '1666fdfc-c4e7-ec11-9130-005056b6948b'
    requirement_supplied_attribute_id = '82a67dea-c4e7-ec11-9130-005056b6948b'
    requirement_available_attribute_id = '9b1a4515-c5e7-ec11-9130-005056b6948b'
    requirement_supply_amount_attribute_id = '376f21de-c4e7-ec11-9130-005056b6948b'
    actual_attribute_value = 'f15978b1-d193-e911-80cd-9783b3495d40'
    # delete_attribute_value = 'd5fa86ec-b9eb-ec11-9131-005056b6948b'
    level_4_attribute_id = '37ddf98d-6bf7-ec11-9134-005056b6948b'
    level_3_attribute_id = '65e17bf4-6bf7-ec11-9134-005056b6948b'
    project_section_attribute_id = '9b1bdb78-d770-e911-8115-817c3f53a992'
    unit_attribute_id = '9904c66d-f66f-e911-8115-817c3f53a992'
    amount_attribute_id = 'fdde6847-c6cf-ea11-9110-005056b6948b'
    weld_attribute_id = '4a32f292-d0df-ec11-912f-005056b6948b'
    diameter_attribute_id = '14e6310b-4356-ec11-911a-005056b6948b'
    document_attribute_id = '5ee448f6-f76f-e911-8115-817c3f53a992'
    construction_attribute_id = '8f3be7b2-ff59-e911-8115-817c3f53a992'
    construction_object_attribute_id = '4f3b1845-4d7c-ed11-9153-005056b6948b'
    construction_subobject_attribute_id = 'ead605bb-5a7c-ed11-9153-005056b6948b'
    available_attribute_id = '9b1a4515-c5e7-ec11-9130-005056b6948b'
    type_attribute_id = '532d2888-3582-ec11-911c-005056b6948b'
    type_supply_attribute_id = 'c7103c3f-7a34-eb11-9110-005056b6948b'
    type_supply_attribute_value = '4fcc60e7-7934-eb11-9110-005056b6948b'
    actual_attribute_id = '0f1c8267-801a-ea11-910b-005056b6948b'
    mass_attribute_id = '7534e5cb-2881-e911-8115-817c3f53a992'
    codes_string_attribute_id = 'da5dd7f2-91eb-ec11-9131-005056b6948b'
    supply_request_list_attribute_id = '78e72aad-c197-ed11-9158-005056b6948b'
    free_available_attribute_id = '67f03111-35ed-ec11-9131-005056b6948b'
    free_total_available_attribute_id = '17a3b446-35ed-ec11-9131-005056b6948b'
    rest_available_attribute_id = 'ca519e0a-35ed-ec11-9131-005056b6948b'
    rest_total_available_attribute_id = '70b4c6e8-34ed-ec11-9131-005056b6948b'
    cad_attribute_id = 'bfef0f53-ae8e-e911-8116-dc30078865da'
    cad_reference_attribute_id = 'f77aec96-d8f5-ec11-9134-005056b6948b'
    mounted_attribute_id = '2d27a85e-9d58-ec11-911a-005056b6948b'
    mounted_spool_attribute_id = '58234b3e-902e-ed11-9143-005056b6948b'
    onsite_storages_attribute_id = 'e27e3c18-7f9c-ed11-9159-005056b6948b'
    onsite_available_attribute_id = '839de02c-809c-ed11-9159-005056b6948b'
    remote_available_attribute_id = '1e2c803f-809c-ed11-9159-005056b6948b'
    # from orders
    order_class_id = 'c776174a-6cfb-ec11-9136-005056b6948b'
    total_delivered_attribute_id = 'f5224d29-d200-ed11-9137-005056b6948b'
    delivered_attribute_id = '6f93288c-6ffb-ec11-9136-005056b6948b'
    total_moving_attribute_id = 'b0cd791b-d200-ed11-9137-005056b6948b'
    moving_attribute_id = '46597676-6ffb-ec11-9136-005056b6948b'
    contractor_attribute_id = '38ee5557-9efe-ec11-9136-005056b6948b'
    order_creation_date_attribute_id = '46aee5d4-2bfc-ec11-9136-005056b6948b'
    # from notification
    notification_class_id = '95655fc4-cc43-ed11-9148-005056b6948b'
    shipped_attribute_id = '406d51d6-f83d-ed11-9147-005056b6948b'
    total_shipped_attribute_id = '682ed6ee-4b50-ed11-914b-005056b6948b'
    delivery_date_attribute_id = '42b74304-823d-ed11-9147-005056b6948b'
    shipping_date_attribute_id = 'e5b80c68-f56f-e911-8115-817c3f53a992'
    # from storages
    storages_class_id = '6e3082bf-c0a2-ed11-915a-005056b6948b'
    storage_id_attribute_id = 'e2e832a2-00f7-ea11-9110-005056b6948b'

    # for related material
    delete_attribute_value = 'd5fa86ec-b9eb-ec11-9131-005056b6948b'
    valid_attribute_values = {
        "Проверить имя": '365a3acd-5b86-ed11-9155-005056b6948b',
        "Проверить код": '153fe32d-5c86-ed11-9155-005056b6948b',
    }

    def __init__(self, session):
        self._session: aiohttp.ClientSession = session

    @staticmethod
    def get_value(attributes: dict, attribute_id: str, attribute_type='str', get_only_id=False):
        result = attributes.get(attribute_id, None)
        if result:
            item_type = result['Type']
            if item_type == 8 and get_only_id:
                return attributes[attribute_id]['Value']['Id']
            elif item_type == 8:
                return attributes[attribute_id]['Value']['Name']
            elif item_type == 3 or item_type == 5:
                value = attributes[attribute_id]['Value']
                return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
            elif item_type == 1:
                return round(attributes[attribute_id]['Value'], 8)
            else:
                return attributes[attribute_id]['Value']
        else:
            if attribute_type == 'int':
                return 0
            elif attribute_type == 'date':
                return None
            else:
                return ''
