import logging
import os
from pathlib import Path


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def folder_creator(folder):

    while True:
        input_path = input(
            f'input the path to create the {folder} folder in: ')
        clear()

        if input_path == '':
            input_path = Path(__file__).parent

        folder_path = Path(input_path/folder)
        try:
            folder_path.mkdir(parents=True, exist_ok=True)
        except (OSError):
            print(
                'you can`t create a folder using invalid characters'
                '\nplease input again using valid characters\n'
            )
            continue
        break

    print(f'{folder} Folder created succefully at '
          f'{folder_path.parent.resolve()}'
          )


folder_creator('source')

folder_creator('replica')
