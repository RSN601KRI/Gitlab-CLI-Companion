import typer
import subprocess
import os
from ..graph.knowledge_graph import kg
from dotenv import load_dotenv
import requests

def post_gitlab_comment(body):
    """
    Post a comment to GitLab Merge Request.
    """
    load_dotenv()
    token = os.getenv('GITLAB_TOKEN')
    base_url = os.getenv('GITLAB_URL', 'https://gitlab.com/api/v4')
    project_id = os.getenv('GITLAB_PROJECT_ID')
    mr_iid = os.getenv('GITLAB_MR_IID')

    if not token:
        typer.echo("Missing GITLAB_TOKEN in .env")
        return False

    if not project_id or not mr_iid:
        typer.echo("Missing GITLAB_PROJECT_ID or GITLAB_MR_IID in .env")
        return False

    # Ensure correct API URL
    if not base_url.endswith('/api/v4'):
        base_url = base_url.rstrip('/') + '/api/v4'

    api_url = f"{base_url}/projects/{project_id}/merge_requests/{mr_iid}/notes"

    headers = {
        "PRIVATE-TOKEN": token
    }

    data = {
        "body": body
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)

        if response.status_code in [200, 201]:
            typer.echo("Comment posted to GitLab MR successfully.")
            return True
        else:
            typer.echo(f"GitLab API Error: {response.status_code}")
            typer.echo(response.text)
            return False

    except requests.exceptions.RequestException as e:
        typer.echo(f"Failed to connect to GitLab: {e}")
        return False

app = typer.Typer()

def get_changed_files():
    """
    Get list of changed files from git.
    
    Uses git status --porcelain to get modified/added files.
    """
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, cwd='.')
        if result.returncode != 0:
            typer.echo("Error running git status. Make sure you're in a git repository.")
            return []
        
        # Parse the output: lines like "M file.py" or "A newfile.py"
        changed_files = []
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                # First two chars are status, rest is filename
                status = line[:2]
                filename = line[2:].strip()
                if status[0] in ['M', 'A', 'D'] or status[1] in ['M', 'A', 'D']:
                    changed_files.append(filename)
        
        return changed_files
    except FileNotFoundError:
        typer.echo("Git not found. Please install git.")
        return []

def get_related_files(changed_files):
    """
    Get related files from knowledge graph for changed files.
    
    Returns set of related file paths.
    """
    related = set()
    for file in changed_files:
        if file in kg.graph:
            # Get all neighbors (related nodes)
            neighbors = kg.get_related_nodes(file)
            for neighbor in neighbors:
                # If neighbor is a file node, add it
                node_info = kg.get_node_info(neighbor)
                if node_info and node_info.get('type') in ['file', 'jenkinsfile', 'gitlab_ci', 'documentation']:
                    related.add(neighbor)
    
    return related

def estimate_blast_radius(changed_count, related_count):
    """
    Estimate blast radius based on number of changes and related files.
    
    Returns: 'Low', 'Medium', 'High'
    """
    total_impacted = changed_count + related_count
    if total_impacted < 3:
        return 'Low'
    elif total_impacted < 6:
        return 'Medium'
    else:
        return 'High'

def calculate_risk_score(changed_count, related_count, blast_radius):
    """
    Calculate risk score 0-10 based on changes and impact.
    
    Higher score = higher risk.
    """
    base_score = min(10, changed_count + related_count)
    
    # Adjust based on blast radius
    if blast_radius == 'High':
        base_score += 2
    elif blast_radius == 'Medium':
        base_score += 1
    
    return min(10, base_score)

@app.callback(invoke_without_command=True)
def review(post: bool = typer.Option(False, "--post", help="Post results to GitLab MR comment")):
    """
    Analyze Merge Request risk by examining changed files and their relationships.
    
    Detects changed files, finds related files from knowledge graph,
    estimates blast radius, and provides risk assessment.
    Use --post to publish results to GitLab Merge Request.
    """
    # Get changed files
    changed_files = get_changed_files()
    if not changed_files:
        typer.echo("No changed files detected.")
        return
    
    # Get related files
    related_files = get_related_files(changed_files)
    
    # Calculate metrics
    files_changed = len(changed_files)
    related_impacted = len(related_files)
    blast_radius = estimate_blast_radius(files_changed, related_impacted)
    risk_score = calculate_risk_score(files_changed, related_impacted, blast_radius)
    
    # Display results
    typer.echo("MR Risk Analysis")
    typer.echo("----------------")
    typer.echo()
    typer.echo(f"Files Changed: {files_changed}")
    typer.echo(f"Related Files Impacted: {related_impacted}")
    typer.echo(f"Estimated Blast Radius: {blast_radius}")
    typer.echo()
    typer.echo(f"Risk Score: {risk_score}/10")
    
    # Suggest files to review
    if related_files:
        typer.echo()
        typer.echo("Suggested files to review:")
        for file in sorted(related_files):
            typer.echo(f"  - {file}")
    
    # Additional advice
    if risk_score >= 7:
        typer.echo("\n[High Risk] Consider breaking this MR into smaller changes.")
    elif risk_score >= 4:
        typer.echo("\n[Medium Risk] Ensure thorough testing of related components.")
    else:
        typer.echo("\n[Low Risk] Changes look contained.")
    
    # Post to GitLab if requested
    if post:
        comment_body = f"""## MR Risk Analysis

**Files Changed:** {files_changed}
**Related Files Impacted:** {related_impacted}
**Estimated Blast Radius:** {blast_radius}

**Risk Score:** {risk_score}/10

"""
        if related_files:
            comment_body += "### Suggested files to review:\n"
            for file in sorted(related_files):
                comment_body += f"- {file}\n"
        
        advice = ""
        if risk_score >= 7:
            advice = "[High Risk] Consider breaking this MR into smaller changes."
        elif risk_score >= 4:
            advice = "[Medium Risk] Ensure thorough testing of related components."
        else:
            advice = "[Low Risk] Changes look contained."
        comment_body += f"\n**{advice}**"
        
        post_gitlab_comment(comment_body)