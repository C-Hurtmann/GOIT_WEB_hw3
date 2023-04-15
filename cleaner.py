from collections import namedtuple
from pathlib import Path
from pprint import pprint

import os


SUFFIX_MAP = {'images':('JPEG', 'PNG', 'JPG', 'SVG'),
              'videos':('AVI', 'MP4', 'MOV', 'MKV'),
              'documents':('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
              'music':('MP3', 'OGG', 'WAV', 'AMR'),
              'archives':('ZIP', 'GZ', 'TAR')}


class FolderContent:
    map = []
    File = namedtuple('File', 'name path new_folder')

    def __init__(self, path='test_folder'):
        self.path = Path(path)

    def overlook(self, path=None):
        if not path:
            path = self.path
        for i in path.iterdir():
            if i.is_file():
                suffix = i.suffix.replace('.', '')
                for folder in SUFFIX_MAP.values():
                    if suffix in folder:
                        self.map.append(self.File(name=i.name, path=i, new_folder=folder))
            else:
                self.overlook(i)
                
def sort(folder_content: FolderContent):
    for folder in SUFFIX_MAP.keys():
        path = os.path.join(folder_content.path, folder)
        os.mkdir(path)
            
    folder_content.map
    pass

path = Path('test_folder')
folder = FolderContent(path)
folder.overlook()

pprint(folder.map)