import argparse
import io
import json
import tarfile
import uuid
import tomli
from pathlib import Path
from reptor.lib.plugins.Base import Base


def dir_path(path):
    p = Path(path)
    if not p.is_dir():
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")
    return p


def build_tarinfo(name, size):
    info = tarfile.TarInfo(name=name)
    info.size = size
    return info


class PackExport(Base):
    meta = {
        "name": "PackExport",
        "summary": "Pack directories into a .tar.gz file",
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.directories: list[Path] = kwargs.get("directories", [])
        self.output = kwargs.get("output")

    @classmethod
    def add_arguments(self, parser, plugin_filepath=None):
        super().add_arguments(parser, plugin_filepath=plugin_filepath)

        parser.add_argument('directories', nargs='+', type=dir_path)
        parser.add_argument('-o', '--output', type=argparse.FileType('wb'))

    def run(self):
        with tarfile.open(fileobj=self.output, mode='w:gz') as tar:
            for path_dir in self.directories:
                # Add NOTICE file at top level, only once per tar.gz file
                notice_path = path_dir / 'NOTICE'
                if notice_path.is_file() and 'NOTICE' not in tar.getnames():
                    tar.add(notice_path, arcname='NOTICE')

                # Add files to archive
                for path_input in list(path_dir.glob('*.toml')) + list(path_dir.glob('*.json')):
                    if not path_input.is_file():
                        continue

                    if path_input.suffix == '.toml':
                        data_dict = tomli.loads(path_input.read_text())
                    else:
                        data_dict = json.loads(path_input.read_text())

                    if not data_dict.get('id'):
                        data_dict['id'] = str(uuid.uuid4())
                    data_json = json.dumps(data_dict, indent=2)
                    tar.addfile(build_tarinfo(name=data_dict['id'] + '.json', size=len(data_json)), fileobj=io.BytesIO(data_json.encode()))
                    
                    # Add files to archive
                    # Translate human-friendly names to archive names based on IDs
                    file_dirs = {}
                    if data_dict.get('format').startswith('projects/'):
                        project_type_id = data_dict.get('project_type', {}).get('id')
                        file_dirs.update({
                            f"{data_dict['id']}-images": f"{data_dict['id']}-images",
                            f"{data_dict['id']}-files": f"{data_dict['id']}-files",
                            f"{project_type_id}-assets": f"{project_type_id}-assets",
                            f"{path_input.stem}-images": f"{data_dict['id']}-images",
                            f"{path_input.stem}-files": f"{data_dict['id']}-files",
                            f"{path_input.stem}-assets": f"{project_type_id}-assets",
                        })
                    elif data_dict.get('format').startswith('projecttypes/'):
                        file_dirs.update({
                            f"{data_dict['id']}-assets": f"{data_dict['id']}-assets",
                            f"{path_input.stem}-assets": f"{data_dict['id']}-assets",
                        })
                    elif data_dict.get('format').startswith('templates/'):
                        file_dirs.update({
                            f"{data_dict['id']}-images": f"{data_dict['id']}-images",
                            f"{path_input.stem}-images": f"{data_dict['id']}-images",
                        })

                    for ds, dd in file_dirs.items():
                        d_dir = Path(path_dir) / ds
                        if d_dir.is_dir():
                            tar.add(d_dir, arcname=dd)


loader = PackExport