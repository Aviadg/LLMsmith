import yaml
import sys

def generate_compose(config_path):
    # Read configuration
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Base compose configuration
    compose = {
        'version': '3.8',
        'services': {},
        'volumes': {}
    }

    # Always include API service
    compose['services']['api'] = {
        'build': '.',
        'ports': [f"{config['api']['port']}:{config['api']['port']}"],
        'volumes': ['.:/app'],
        'environment': ['CONFIG_PATH=/app/config.yaml'],
        'depends_on': []
    }

    # Add services based on configuration
    if config['services']['url_to_markdown']:
        compose['services']['urltomarkdown'] = {
            'build': {
                'context': '.',
                'dockerfile': 'Dockerfile.urltomarkdown'
            },
            'ports': [f"{config['url_to_markdown']['exposed_port']}:{config['url_to_markdown']['port']}"],
            'environment': [f"PORT={config['url_to_markdown']['port']}"]
        }
        compose['services']['api']['depends_on'].append('urltomarkdown')

    if config['services']['redis']:
        compose['services']['redis'] = {
            'image': 'redis:alpine',
            'ports': [f"{config['redis']['exposed_port']}:{config['redis']['port']}"],
            'volumes': ['redis_data:/data'],
            'command': 'redis-server --appendonly yes'
        }
        compose['volumes']['redis_data'] = None
        compose['services']['api']['depends_on'].append('redis')

    if config['services']['qdrant']:
        compose['services']['qdrant'] = {
            'image': 'qdrant/qdrant',
            'ports': [f"{config['qdrant']['exposed_port']}:{config['qdrant']['port']}"],
            'volumes': ['qdrant_data:/qdrant/storage']
        }
        compose['volumes']['qdrant_data'] = None
        compose['services']['api']['depends_on'].append('qdrant')

    if config['services']['postgres']:
        compose['services']['postgres'] = {
            'image': 'postgres:13-alpine',
            'ports': [f"{config['postgres']['exposed_port']}:{config['postgres']['port']}"],
            'environment': [
                f"POSTGRES_DB={config['postgres']['database']}",
                f"POSTGRES_USER={config['postgres']['user']}",
                f"POSTGRES_PASSWORD={config['postgres']['password']}"
            ],
            'volumes': ['postgres_data:/var/lib/postgresql/data']
        }
        compose['volumes']['postgres_data'] = None
        compose['services']['api']['depends_on'].append('postgres')

    # Write docker-compose.yml
    with open('docker-compose.yml', 'w') as f:
        yaml.dump(compose, f, default_flow_style=False)

if __name__ == "__main__":
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.yaml"
    generate_compose(config_path)