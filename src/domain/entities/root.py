from dataclasses import dataclass, field


@dataclass
class Root:

    name: str
    root_id: str
    cost_center_code: str = None
    parent_root: str = None
    construction_object: str = None
    onsite_storage_ids: list = field(default_factory=list)
