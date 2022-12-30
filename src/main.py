import sys
from datetime import datetime
from application.controllers import ManageAllMainRoots, ManageMainRoot, ManageChildRoot, ExportAllRequirements

# При релизе версии нужно ставить в переменную debug значение false
DEBUG = False


def debug():
    mode = 'validation'
    main_root_id = ''
    child_root_id = 'c470a234-e559-11ec-9136-005056b6c24b'
    if main_root_id:
        ManageMainRoot().execute(mode, main_root_id)
    elif child_root_id:
        ManageChildRoot().execute(mode, child_root_id)


def manage(mode):
    if mode == 'export':
        ExportAllRequirements().execute()
    else:
        ManageAllMainRoots().execute(mode)


def manual():
    modes = {
        1: 'distribution',
        2: 'deleting',
        3: 'normalization',
        4: 'validation',
        5: 'export',
    }
    controllers = {
        1: 'all',
        2: 'main',
        3: 'child'
    }
    print('Выберете действие')
    print(*[f'{item[1]} - {item[0]}' for item in modes.items()], sep='\n')
    mode_number = None
    while mode_number is None:
        s = input('Введите: ')
        if s.isdigit() and modes.get(int(s)):
            mode_number = int(s)
        else:
            print('Не удалось распознать запрос')

    mode = modes.get(mode_number, 'not determine')

    if mode == 'export':
        input('Будет выполнен экспорт всех потребностей в эксель файл. Для начала обработки нажмите Ввод')
        ExportAllRequirements().execute()
    else:
        print('Объекты для обработки')
        print(*[f'{item[1]} - {item[0]}' for item in controllers.items()], sep='\n')
        controller_number = None
        while controller_number is None:
            s = input('Введите: ')
            if s.isdigit() and controllers.get(int(s)):
                controller_number = int(s)
            else:
                print('Не удалось распознать запрос')

        controller = controllers.get(controller_number, 'not determine')

        print(mode, controller)
        if controller == 'all':
            input('Для начала обработки нажмите Ввод')
            ManageAllMainRoots().execute(mode)
        elif controller == 'main':
            print('Указание идентификатора стройки для обработки')
            main_root_id = input('Указание id: ')
            ManageMainRoot().execute(mode, main_root_id)
        elif controller == 'child':
            print('Указание идентификатора титула для обработки')
            child_root_id = input('Указание титула: ')
            ManageChildRoot().execute(mode, child_root_id)

    input('Для завершения нажмите Ввод')


if __name__ == '__main__':
    start_time = datetime.now()

    if DEBUG:
        debug()
    elif len(sys.argv) == 2:
        manage(sys.argv[1])
    else:
        manual()

    print(f'Total duration {datetime.now() - start_time}')
