from collections import namedtuple
from pathlib import Path
import os
import shutil


SUFFIX_MAP = {'images':('JPG', 'PNG', 'JPG', 'SVG'),
              'videos':('AVI', 'MP4', 'MOV', 'MKV'),
              'documents':('DOC', 'DOCX', 'TXT', 'PDF', 'XLS', 'PPTX'),
              'music':('MP3', 'OGG', 'WAV', 'AMR'),
              'archives':('ZIP', 'GZ', 'TAR'),
              'unknown':...}


class FolderContent:
    File = namedtuple('File', 'name path new_folder')

    def __init__(self, path):
        self.path = path
        self.map = []
        self.__overlook(path)

    def __define_folder(self, file):
        suffix = file.suffix.replace('.', '').upper()
        for k, v in SUFFIX_MAP.items():
            if suffix in v:
                return k
        else:
            return 'unknown'

    def __overlook(self, path=None):
        if not path:
            path = self.path
        for i in path.iterdir():
            if i.is_file():
                self.map.append(self.File(name=i.name, path=i, new_folder=self.__define_folder(i)))
            else:
                self.__overlook(i)
    
    def _define_spare_folders(self):
        subfolders = [i for i in self.path.iterdir() if i.is_dir()]
        return [i for i in subfolders if i.name not in list(SUFFIX_MAP.keys())]

class Sorter:
    def __init__(self, folder):
        self.__folder = FolderContent(folder)

    def __sort(self):
            for i in self.__folder.map:  
                new_folder_path = os.path.join(self.__folder.path, i.new_folder)
                os.makedirs(new_folder_path, exist_ok=True)
                os.replace(i.path, os.path.join(new_folder_path, i.name))

    def __delete_spare_folders(self):
        for i in self.__folder._define_spare_folders():
            shutil.rmtree(i)

    def run(self):
        self.__sort()
        self.__delete_spare_folders()
        print(f'Folder {self.__folder.path.name} has been sorted successfully')


if __name__ == '__main__':
    folder = FolderContent(Path('test_folder'))
    sorter = Sorter(Path('test_folder'))
    sorter.run()
 