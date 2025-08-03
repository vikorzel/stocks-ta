import typing
import os
import pathlib
import json

class AppConfig(typing.TypedDict):
    static_folder: str
    template_folder: str
    version: str
    llmModel: str
    llmMaxTokens: int
    
def get_app_config() -> AppConfig:
    script_path = pathlib.Path(__file__).resolve()
    pdir = script_path.parent.parent
    version_file = pathlib.Path(pdir, 'version.txt')
    if not version_file.exists():
        raise FileNotFoundError(f"Version file not found at {version_file}")
    with open(version_file, 'r') as vf:
        version = vf.read().strip()
    
    config_path = os.getenv('TA_APP_CONFIG', pdir.joinpath('config.json').as_posix())
    config_data = json.loads(open(config_path, 'r').read())
    return AppConfig(
        static_folder=config_data['path']['static'],
        template_folder=config_data['path']['template'],
        version=version,
        llmModel=config_data['llm']['model'],
        llmMaxTokens=config_data['llm']['max_tokens']
    )