import logging,os,yaml
logger = logging.getLogger(__name__)


def load_yaml_file(file_path):
    with open(file_path, 'r') as file:
        if os.path.exists(file_path):
            logger.info(f"Loaded configuration from {file_path}")
            return yaml.safe_load(file)
        else:
            logger.warning(f"Configuration file not found: {file_path}")
            return {}            

def load_configs(config_file):
    if os.path.exists(config_file):
        config = load_yaml_file(config_file)
        include_dir = config.get('include_dir')
        if include_dir and os.path.isdir(include_dir):
            # List all .yaml files in the include_dir
            for filename in os.listdir(include_dir):
                if filename.endswith('.yaml'):
                    file_path = os.path.join(include_dir, filename)
                    extra_config = load_yaml_file(file_path)
                    
                    # Merge extra config into the main config
                    config.update(extra_config)
    else:
        logger.warning(f"Configuration file not found: {config_file}")
        return {}

    return config



VERSION = 'OutLine Manager 1.0'
DESCRIPTION = "Erfan Outline Manager"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, '..' ,'config.yaml')
CONFIG = load_configs(CONFIG_FILE)
DB_NAME = CONFIG['database']['name']

