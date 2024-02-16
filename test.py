import logging
import os
import shutil
from pathlib import Path

source_files = []
replica_files = []


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

        folder_path = Path(input_path) / folder
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

    return folder_path


source_folder = folder_creator('source')

replica_folder = folder_creator('replica')

logs_folder = folder_creator('logs')


def make_log(operation):
    logging.basicConfig(
        filename=logs_folder.joinpath('operations.log'),
        filemode='a',
        format='%(levelname)s - %(asctime)s - %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.info(f'a file was {operation}')


for source_file in source_folder.glob('*'):
    source_files.append(source_file.name)

for replica_file in replica_folder.glob('*'):
    replica_files.append(replica_file.name)

for source_file in source_folder.glob('*'):
    if source_file.name in replica_files:
        continue
    else:
        if source_file.is_file():
            shutil.copy(source_file, replica_folder)
        elif source_file.is_dir():
            shutil.copytree(source_file, replica_folder/source_file.name)


for replica_file in replica_folder.glob('*'):
    if replica_file.name in source_files:
        continue
    else:
        if replica_file.is_file():
            Path.unlink(replica_file)
        elif replica_file.is_dir():
            shutil.rmtree(replica_file)

make_log('erased')
make_log('copied')
make_log('created')

# sinc = input('input the sincronization interval')
