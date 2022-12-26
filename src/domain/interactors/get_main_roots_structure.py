class GetMainRootsStructure:

    def __init__(self, main_root_repository, child_root_repository):
        self._main_root_repository = main_root_repository
        self._child_roots_repository = child_root_repository

    def execute(self) -> list[dict]:
        """Метод возвращает список словарей с ключами main_root, child_roots и значениями в виде экземпляров Root"""
        main_roots = self._main_root_repository.get()
        result = list()
        for main_root in main_roots:
            result.append({
                'main_root': main_root,
                'child_roots': self._child_roots_repository.get_by_main_root(main_root)
            })
        return result
