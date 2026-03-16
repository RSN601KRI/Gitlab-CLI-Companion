import typer
import os
from collections import Counter
from ..graph.knowledge_graph import update_graph_from_docs

app = typer.Typer()

def analyze_repo_structure():
    """
    Analyze the repository structure.
    
    Returns a dict with folders, files, and language detection.
    """
    structure = {
        'folders': [],
        'files': [],
        'language': 'Unknown'
    }
    
    # Get root contents
    try:
        items = os.listdir('.')
        for item in items:
            if os.path.isdir(item) and not item.startswith('.'):
                structure['folders'].append(item)
            elif os.path.isfile(item):
                structure['files'].append(item)
    except Exception as e:
        typer.echo(f"Error analyzing repo: {e}")
        return structure
    
    # Detect main language by file extensions
    extensions = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if not file.startswith('.') and '.' in file:
                ext = file.split('.')[-1].lower()
                extensions.append(ext)
    
    ext_counts = Counter(extensions)
    if ext_counts:
        main_ext = ext_counts.most_common(1)[0][0]
        lang_map = {
            'py': 'Python',
            'js': 'JavaScript',
            'ts': 'TypeScript',
            'java': 'Java',
            'go': 'Go',
            'rs': 'Rust',
            'cpp': 'C++',
            'c': 'C'
        }
        structure['language'] = lang_map.get(main_ext, main_ext.upper())
    
    return structure

def generate_readme(structure):
    """
    Generate README.md content.
    """
    content = f"""# GitLab DevOps Companion CLI (glc)

A production-ready CLI tool to assist with GitLab DevOps workflows.

## Features

- **migrate**: Convert Jenkins pipeline to GitLab CI
- **scan**: Security scan for secrets and insecure CI configs
- **docs**: Auto-generate documentation (this command)
- **health**: Repo health dashboard
- **review**: Analyze Merge Request risk

## Folder Structure

"""
    
    for folder in sorted(structure['folders']):
        content += f"- **{folder}/**: [Description needed]\n"
    
    content += """

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd gitlab-devops-companion
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
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
"""
    return content

def generate_contributing():
    """
    Generate CONTRIBUTING.md content.
    """
    content = """# Contributing to GitLab DevOps Companion CLI

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## How to Contribute

1. **Fork the repository** on GitHub
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes** following the code style
4. **Add tests** if applicable
5. **Commit your changes**: `git commit -m "Add your message"`
6. **Push to your branch**: `git push origin feature/your-feature-name`
7. **Create a Pull Request**

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions
- Keep functions small and focused

## Testing

Run tests before submitting:
```bash
python -m pytest
```

## Reporting Issues

- Use GitHub Issues to report bugs
- Provide detailed steps to reproduce
- Include relevant error messages and logs

## Code of Conduct

Please be respectful and constructive in all interactions.
"""
    return content

def generate_architecture():
    """
    Generate ARCHITECTURE.md content with Mermaid diagram.
    """
    content = """# System Architecture

This document describes the high-level architecture of the GitLab DevOps Companion CLI.

## Overview

The CLI is built as a modular Python application using Typer for command-line interface management.

## Architecture Diagram

```mermaid
graph TD
    A[Repository] --> B[CLI Entry Point]
    B --> C[Commands Module]
    C --> D[Migrate Command]
    C --> E[Scan Command]
    C --> F[Docs Command]
    C --> G[Health Command]
    C --> H[Review Command]
    
    B --> I[Graph Module]
    I --> J[Knowledge Graph]
    
    B --> K[Utils Module]
    K --> L[Git Utils]
    K --> M[File Utils]
    
    B --> N[Config Module]
    
    D --> O[GitLab CI Generation]
    E --> P[Security Scanning]
    F --> Q[Documentation Generation]
```

## Components

- **CLI Entry Point**: Main application entry using Typer
- **Commands Module**: Individual command implementations
- **Graph Module**: Knowledge graph utilities using NetworkX
- **Utils Module**: Helper functions for Git and file operations
- **Config Module**: Configuration management

## Data Flow

1. User runs CLI command
2. Typer routes to appropriate command handler
3. Command processes repository data
4. Results are displayed or files are generated
"""
    return content

@app.callback(invoke_without_command=True)
def docs():
    """
    Auto-generate repository documentation.
    
    Analyzes the repository structure, detects the main programming language,
    and generates README.md, CONTRIBUTING.md, and ARCHITECTURE.md files.
    """
    typer.echo("Analyzing repository structure...")
    
    # Analyze repo
    structure = analyze_repo_structure()
    
    typer.echo(f"Detected main language: {structure['language']}")
    typer.echo(f"Found {len(structure['folders'])} major folders")
    
    # Generate documentation files
    files_to_generate = [
        ('README.md', generate_readme(structure)),
        ('CONTRIBUTING.md', generate_contributing()),
        ('ARCHITECTURE.md', generate_architecture())
    ]
    
    for filename, content in files_to_generate:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            typer.echo(f"Generated {filename}")
        except Exception as e:
            typer.echo(f"Error generating {filename}: {e}")
    
    # Update knowledge graph
    update_graph_from_docs([filename for filename, _ in files_to_generate])
    
    typer.echo("Documentation generation complete!")