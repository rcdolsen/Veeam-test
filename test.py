import logging
import os
import shutil
import time
from pathlib import Path


# function to clear the console
def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


# function to create the folders
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
          f'{folder_path.parent.resolve()}\n'
          )

    return folder_path


# using the function folder_creator to create the folder "source"
source_folder = folder_creator('source')

# using the function folder_creator to create the folder "replica"
replica_folder = folder_creator('replica')

# using the function folder_creator to create the folder "logs"
logs_folder = folder_creator('logs')

while True:
    try:
        sinc_time = float(
            input('input the sincronization interval in seconds: '))
        clear()
    except ValueError:
        print('please input a number\n')
        continue
    if sinc_time <= 0:
        print('please input a positive non-zero number')
    else:
        break


# function to create the log file and the infos inside
def make_log(operation, file, f_d):
    print("loguei mane")
    logging.basicConfig(
        filename=logs_folder.joinpath('operations.log'),
        filemode='a',
        format='%(levelname)s - %(asctime)s \n%(message)s\n',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.info(f'the {f_d} "{file}" was {operation} the replica folder')


# Iterates over the folders to check if the files exist in both folders
def make_sinc():
    source_files = []
    replica_files = []

    # saves the names of the files in source_file in a list
    for source_file in source_folder.glob('*'):
        source_files.append(source_file.name)

    # saves the names of the files in replica_file in a list
    for replica_file in replica_folder.glob('*'):
        replica_files.append(replica_file.name)

    for source_file in source_folder.glob('*'):
        if source_file.name in replica_files:
            for replica_file in replica_folder.glob('*'):

                # if the files exist in both folders check if they have the
                # same name and have been altered
                if replica_file.name == source_file.name:
                    if source_file.stat().st_mtime == replica_file.stat().st_mtime:
                        continue
                    # replaces the file if it have been altered
                    else:
                        if source_file.is_file():
                            shutil.copy2(source_file, replica_folder)
                            make_log('replaced in', source_file.name, 'file')
                        else:
                            shutil.rmtree(replica_file)
                            shutil.copytree(
                                source_file, replica_folder/source_file.name)
                            make_log('replaced in', source_file.name, 'file')
                else:
                    continue
        # copies the file in source folder to replica folder if it does not
        # exist
        else:
            if source_file.is_file():
                shutil.copy2(source_file, replica_folder)
                make_log('created in', source_file.name, 'file')
            # elif source_file.is_dir():
            else:
                shutil.copytree(source_file, replica_folder/source_file.name)
                make_log('created in', source_file.name, 'folder')

    # iterates over replica folder and removes the files that does not exist in
    # source folder
    for replica_file in replica_folder.glob('*'):
        if replica_file.name in source_files:
            continue
        else:
            if replica_file.is_file():
                Path.unlink(replica_file)
                make_log('erased from', replica_file.name, 'file')

            elif replica_file.is_dir():
                shutil.rmtree(replica_file)
                make_log('erased from', replica_file.name, 'folder')


# Function to synchronize files at regular intervals
def sinc_exec():
    while True:
        make_sinc()
        time.sleep(sinc_time)


# Start synchronization
sinc_exec()
