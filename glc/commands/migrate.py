import typer
import os
import re
import yaml
from ..graph.knowledge_graph import update_graph_from_migrate

app = typer.Typer()

@app.callback(invoke_without_command=True)
def migrate():
    """
    Convert Jenkins pipeline to GitLab CI.

    This command detects a Jenkinsfile in the repository root,
    parses the stages defined in it, and generates a corresponding
    .gitlab-ci.yml file with GitLab CI jobs.
    """
    # Step 1: Detect Jenkinsfile in repo root
    jenkinsfile_path = 'Jenkinsfile'
    if not os.path.exists(jenkinsfile_path):
        typer.echo("No Jenkinsfile found in the repository root.")
        return

    # Step 2: Read and parse the Jenkinsfile
    try:
        with open(jenkinsfile_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        typer.echo(f"Error reading Jenkinsfile: {e}")
        return

    # Step 3: Parse stages using regex
    # Look for patterns like stage('Build'), stage('Test'), etc.
    stages = re.findall(r"stage\('([^']+)'\)", content)
    if not stages:
        typer.echo("No stages found in Jenkinsfile. Ensure stages are defined as stage('Stage Name').")
        return

    # Step 4: Convert stages to GitLab CI jobs
    gitlab_jobs = {}
    for stage in stages:
        # Create job name by lowercasing and replacing spaces with underscores
        job_name = stage.lower().replace(' ', '_')
        # Create job definition with stage and placeholder script
        gitlab_jobs[job_name] = {
            'stage': stage.lower(),
            'script': [f'echo "Run commands for {stage}"']  # Placeholder script
        }

    # Step 5: Output generated .gitlab-ci.yml
    try:
        with open('.gitlab-ci.yml', 'w', encoding='utf-8') as f:
            yaml.dump(gitlab_jobs, f, default_flow_style=False, sort_keys=False)
    except Exception as e:
        typer.echo(f"Error writing .gitlab-ci.yml: {e}")
        return

    # Step 6: Update knowledge graph
    update_graph_from_migrate(jenkinsfile_path, '.gitlab-ci.yml', stages)

    # Step 7: Show migration summary
    typer.echo("Pipeline Migration Summary")
    typer.echo("--------------------------")
    typer.echo(f"Jenkins Stages Found: {len(stages)}")
    typer.echo(f"GitLab Jobs Generated: {len(gitlab_jobs)}")
    typer.echo("File Created: .gitlab-ci.yml")