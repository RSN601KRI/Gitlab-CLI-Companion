import typer
import os
import re
from rich.table import Table
from rich.console import Console
from ..graph.knowledge_graph import update_graph_from_scan
from dotenv import load_dotenv
import requests

def post_gitlab_comment(body):
    """
    Post a comment to GitLab Merge Request.
    """
    load_dotenv()
    token = os.getenv('GITLAB_TOKEN')
    url = os.getenv('GITLAB_URL', 'https://gitlab.com')
    project_id = os.getenv('GITLAB_PROJECT_ID')
    mr_iid = os.getenv('GITLAB_MR_IID')
    
    if not all([token, project_id, mr_iid]):
        typer.echo("GitLab integration not configured. Set GITLAB_TOKEN, GITLAB_PROJECT_ID, GITLAB_MR_IID in .env")
        return False
    
    api_url = f"{url}/api/v4/projects/{project_id}/merge_requests/{mr_iid}/notes"
    headers = {'Authorization': f'Bearer {token}'}
    data = {'body': body}
    
    try:
        response = requests.post(api_url, headers=headers, data=data)
        response.raise_for_status()
        typer.echo("Comment posted to GitLab MR successfully.")
        return True
    except requests.exceptions.RequestException as e:
        typer.echo(f"Failed to post comment to GitLab: {e}")
        return False

app = typer.Typer()

# Define secret patterns to detect
SECRET_PATTERNS = {
    'API_KEY': re.compile(r'API_KEY\s*[:=]\s*["\']?([^"\']+)["\']?', re.IGNORECASE),
    'SECRET': re.compile(r'SECRET\s*[:=]\s*["\']?([^"\']+)["\']?', re.IGNORECASE),
    'PASSWORD': re.compile(r'PASSWORD\s*[:=]\s*["\']?([^"\']+)["\']?', re.IGNORECASE),
    'AWS_ACCESS_KEY_ID': re.compile(r'AWS_ACCESS_KEY_ID\s*[:=]\s*["\']?([^"\']+)["\']?', re.IGNORECASE),
    'AWS_SECRET_ACCESS_KEY': re.compile(r'AWS_SECRET_ACCESS_KEY\s*[:=]\s*["\']?([^"\']+)["\']?', re.IGNORECASE),
}

# Define risky CI patterns
RISKY_CI_PATTERNS = {
    'Plaintext Secret': re.compile(r'(API_KEY|SECRET|PASSWORD|AWS_.*_KEY)\s*[:=]\s*["\']?([^"\']+)["\']?', re.IGNORECASE),
    'Overly Permissive': re.compile(r'chmod\s+777', re.IGNORECASE),
}

def scan_file_for_secrets(file_path):
    """
    Scan a file for hardcoded secrets using predefined patterns.
    
    Returns a list of findings with file, line, issue, and severity.
    """
    findings = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line_num, line in enumerate(lines, 1):
            for pattern_name, regex in SECRET_PATTERNS.items():
                if regex.search(line):
                    findings.append({
                        'file': file_path,
                        'line': line_num,
                        'issue': f'Hardcoded {pattern_name}',
                        'severity': 'High'
                    })
    except Exception as e:
        typer.echo(f"Error scanning {file_path}: {e}")
    
    return findings

def scan_file_for_ci_risks(file_path):
    """
    Scan a file for insecure CI configuration patterns.
    
    Returns a list of findings with file, line, issue, and severity.
    """
    findings = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line_num, line in enumerate(lines, 1):
            for pattern_name, regex in RISKY_CI_PATTERNS.items():
                if regex.search(line):
                    findings.append({
                        'file': file_path,
                        'line': line_num,
                        'issue': pattern_name,
                        'severity': 'Medium' if 'Permissive' in pattern_name else 'High'
                    })
    except Exception as e:
        typer.echo(f"Error scanning {file_path}: {e}")
    
    return findings

def calculate_security_score(findings):
    """
    Calculate a security score based on findings.
    
    High severity: -20 points, Medium: -10 points.
    Score ranges from 0 to 100.
    """
    score = 100
    for finding in findings:
        if finding['severity'] == 'High':
            score -= 20
        elif finding['severity'] == 'Medium':
            score -= 10
    return max(0, score)

@app.callback(invoke_without_command=True)
def scan(post: bool = typer.Option(False, "--post", help="Post results to GitLab MR comment")):
    """
    Perform security scan for secrets and insecure CI configurations.
    
    Scans specified files for hardcoded secrets and risky patterns,
    then displays results in a formatted table and summary report.
    Use --post to publish results to GitLab Merge Request.
    """
    # Define files to scan
    files_to_scan = ['.env', '.gitlab-ci.yml', 'config.json', 'config.py']
    
    # Collect all findings
    all_findings = []
    for file_path in files_to_scan:
        if os.path.exists(file_path):
            typer.echo(f"Scanning {file_path}...")
            all_findings.extend(scan_file_for_secrets(file_path))
            if file_path.endswith('.yml') or file_path.endswith('.yaml'):
                all_findings.extend(scan_file_for_ci_risks(file_path))
    
    # Update knowledge graph
    update_graph_from_scan(all_findings)
    
    # Display results in a table
    console = Console()
    table = Table(title="Security Scan Findings")
    table.add_column("File", style="cyan", no_wrap=True)
    table.add_column("Line", style="magenta", justify="right")
    table.add_column("Issue", style="red")
    table.add_column("Severity", style="yellow")
    
    for finding in all_findings:
        table.add_row(
            finding['file'],
            str(finding['line']),
            finding['issue'],
            finding['severity']
        )
    
    if all_findings:
        console.print(table)
    else:
        typer.echo("No security issues found!")
    
    # Calculate summary statistics
    secrets_found = len([f for f in all_findings if 'Hardcoded' in f['issue']])
    risky_configs = len([f for f in all_findings if f['issue'] in ['Plaintext Secret', 'Overly Permissive']])
    security_score = calculate_security_score(all_findings)
    
    # Display summary report
    typer.echo("\nSecurity Scan Report")
    typer.echo("--------------------")
    typer.echo(f"Secrets detected: {secrets_found}")
    typer.echo(f"Risky CI configs: {risky_configs}")
    typer.echo(f"Security Score: {security_score}/100")
    
    # Post to GitLab if requested
    if post:
        comment_body = f"""## Security Scan Result

**Security Score:** {security_score}/100
**Secrets Found:** {secrets_found}
**Risky CI Configs:** {risky_configs}

"""
        if all_findings:
            comment_body += "### Findings:\n"
            for finding in all_findings:
                comment_body += f"- **{finding['file']}:{finding['line']}** - {finding['issue']} ({finding['severity']})\n"
        else:
            comment_body += "✅ No security issues found!\n"
        
        post_gitlab_comment(comment_body)