import yaml
import sys

def generate_compose(config_path):
    # Read configuration
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Base compose configuration
    compose = {
        'services': {},
        'volumes': {}
    }

    exposed_api_port = config.get('api', {}).get('port', 8000)
    # Always include API service
    compose['services']['api'] = {
        'build': '.',
        'ports': [f"{exposed_api_port}:8000"],
        'volumes': ['.:/app'],
        'environment': [
            'CONFIG_PATH=/app/config.yaml',
            f"OPENAI_API_KEY={config['openai']['api_key']}"
        ],
        'depends_on': []
    }

    # Add services based on configuration
    if config['services']['url_to_markdown']:
        exposed_url_to_markdown_port = config.get('url_to_markdown', {}).get('port', 1337)
        compose['services']['urltomarkdown'] = {
            'build': {
                'context': '.',
                'dockerfile': 'Dockerfile.urltomarkdown'
            },
            'ports': [f"{exposed_url_to_markdown_port}:1337"],
            'environment': ['PORT=1337']
        }
        compose['services']['api']['depends_on'].append('urltomarkdown')

    if config['services']['redis']:
        compose['services']['redis'] = {
            'image': 'redis:alpine',
            'ports': [f"{config['redis']['port']}:6379"],
            'volumes': ['redis_data:/data'],
            'command': 'redis-server --appendonly yes'
        }
        compose['volumes']['redis_data'] = None
        compose['services']['api']['depends_on'].append('redis')

    if config['services']['qdrant']:
        compose['services']['qdrant'] = {
            'image': 'qdrant/qdrant',
            'ports': [f"{config['qdrant']['port']}:6333"],
            'volumes': ['qdrant_data:/qdrant/storage']
        }
        compose['volumes']['qdrant_data'] = None
        compose['services']['api']['depends_on'].append('qdrant')

    if config['services']['postgres']:
        compose['services']['postgres'] = {
            'image': 'postgres:13-alpine',
            'ports': [f"{config['postgres']['port']}:5432"],
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