# LLMsmith 🛠️

LLMsmith is a Swiss Army Knife for working with Large Language Models. It provides a unified toolkit that combines essential services for data processing, conversion, and storage in LLM workflows.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features 🌟

- **Speech-to-Text** - Convert audio files to text using OpenAI's advanced models
- **Document Conversion** - Transform various document formats to markdown using [markitdown](https://github.com/microsoft/markitdown)
- **URL to Markdown** - Convert web pages to markdown using [urltomarkdown](https://github.com/macsplit/urltomarkdown)
- **Persistent Storage** - Built-in support for Redis, Qdrant, and PostgreSQL
- **Easy Configuration** - Simple YAML configuration for customizing services and ports
- **Docker-based** - One command to run everything

## Quick Start 🚀

### Default Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/llmsmith
cd llmsmith

# Set your OpenAI API key in config.yaml
# Start all services
docker compose up
```

### Custom Setup

1. Edit `config.yaml` to enable/disable services and customize ports:

```yaml
services:
  speech_to_text: true
  markdown_converter: true
  url_to_markdown: true
  redis: true
  qdrant: true
  postgres: true

# Configure ports and credentials...
```

2. Use the start script for custom configuration:

```bash
./start.sh
```

## API Endpoints 📡

Once running, access the Swagger documentation at: `http://localhost:8000/docs`

### Main Endpoints

- `POST /speech-to-text/transcribe` - Convert audio to text
- `POST /speech-to-text/translate` - Translate audio to English
- `POST /markdown/convert` - Convert documents to markdown
- `GET /url-to-markdown/convert` - Convert webpage to markdown

## Service Ports 🔌

Default ports (customizable via config.yaml):

- FastAPI: 8000
- URL to Markdown: 1337
- Redis: 6379
- Qdrant: 6333
- PostgreSQL: 5432

## Configuration 🔧

LLMsmith can be configured through `config.yaml`. You can:

- Enable/disable specific services
- Customize exposed ports
- Set database credentials
- Configure API keys

Example configuration:

```yaml
services:
  speech_to_text: true
  markdown_converter: true
  url_to_markdown: true
  redis: true
  qdrant: true
  postgres: true

api:
  port: 8000

redis:
  exposed_port: 6379  # Change if you have conflicts

# ... other configurations
```

## Development 🔨

Requirements:
- Docker
- Docker Compose
- Python 3.11+ (for local development)

Local development setup:

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Format code
black .
```

## Credits 👏

LLMsmith integrates several excellent open-source projects:

- [markitdown](https://github.com/microsoft/markitdown) - Document conversion
- [urltomarkdown](https://github.com/macsplit/urltomarkdown) - Web page conversion
- [Qdrant](https://github.com/qdrant/qdrant) - Vector database
- [OpenAI API](https://platform.openai.com/) - Speech-to-text capabilities

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.