# GitLab DevOps Companion CLI (glc)

A production-ready CLI tool to assist with GitLab DevOps workflows.

## Features

- **migrate**: Convert Jenkins pipeline to GitLab CI
- **scan**: Security scan for secrets and insecure CI configs
- **docs**: Auto-generate documentation (this command)
- **health**: Repo health dashboard
- **review**: Analyze Merge Request risk

## Folder Structure

- **__pycache__/**: [Description needed]
- **glc/**: [Description needed]
- **glc.egg-info/**: [Description needed]


## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd gitlab-devops-companion
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the CLI:
   ```bash
   python -m glc.main --help
   ```

## Usage

```bash
# Migrate Jenkins to GitLab CI
python -m glc.main migrate

# Security scan
python -m glc.main scan

# Generate documentation
python -m glc.main docs
```

## Development

This project is written in {structure['language']}.

## License

[Add license information]
