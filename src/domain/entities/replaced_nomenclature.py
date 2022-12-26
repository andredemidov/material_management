from dataclasses import dataclass, field


@dataclass
class ReplacedNomenclature:
    related_materials: list = field(default_factory=list)
