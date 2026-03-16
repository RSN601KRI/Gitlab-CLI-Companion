import typer
import os
import yaml
from rich.console import Console
from rich.text import Text
from ..graph.knowledge_graph import kg

app = typer.Typer()

def calculate_security_score():
    """
    Calculate security score from knowledge graph.
    
    Returns score 0-100 based on security issues.
    """
    security_issues = kg.get_all_nodes_by_type('security_issue')
    high_severity = sum(1 for node in security_issues 
                       if kg.get_node_info(node).get('severity') == 'High')
    medium_severity = sum(1 for node in security_issues 
                         if kg.get_node_info(node).get('severity') == 'Medium')
    
    # Deduct 20 points per high, 10 per medium
    score = 100 - (high_severity * 20) - (medium_severity * 10)
    return max(0, score)

def calculate_doc_coverage():
    """
    Calculate documentation coverage percentage.
    
    Based on documentation nodes vs total files in graph.
    """
    docs = kg.get_all_nodes_by_type('documentation')
    files = kg.get_all_nodes_by_type('file') + kg.get_all_nodes_by_type('jenkinsfile') + kg.get_all_nodes_by_type('gitlab_ci')
    
    if not files:
        return 0
    
    # Simple ratio: docs / files * 100, but cap at 100
    coverage = min(100, len(docs) / len(files) * 100)
    return int(coverage)

def check_pipeline_validity():
    """
    Check if .gitlab-ci.yml is valid YAML.
    
    Returns 'Valid' or 'Invalid'.
    """
    gitlab_ci_path = '.gitlab-ci.yml'
    if not os.path.exists(gitlab_ci_path):
        return 'Missing'
    
    try:
        with open(gitlab_ci_path, 'r', encoding='utf-8') as f:
            yaml.safe_load(f)
        return 'Valid'
    except yaml.YAMLError:
        return 'Invalid'

def get_mr_risk_level():
    """
    Get MR risk level.
    
    Placeholder: returns 'Low' for now.
    TODO: Implement actual MR analysis.
    """
    return 'Low'

def get_colored_score(score, max_score=100):
    """
    Return colored text for score.
    
    Green for >=80, Yellow for 50-79, Red for <50.
    """
    if score >= 80:
        color = "green"
    elif score >= 50:
        color = "yellow"
    else:
        color = "red"
    
    return f"[{color}]{score}[/{color}]"

def get_colored_status(status):
    """
    Return colored text for status.
    
    Green for Valid/Good, Red for Invalid/Bad.
    """
    if status in ['Valid', 'Low']:
        color = "green"
    elif status in ['Invalid', 'Missing', 'High']:
        color = "red"
    else:
        color = "yellow"
    
    return f"[{color}]{status}[/{color}]"

@app.callback(invoke_without_command=True)
def health():
    """
    Display repository health dashboard.
    
    Shows security score, documentation coverage, pipeline validity, and MR risk level.
    Uses data from knowledge graph if available.
    """
    console = Console()
    
    # Calculate metrics
    security_score = calculate_security_score()
    doc_coverage = calculate_doc_coverage()
    pipeline_status = check_pipeline_validity()
    mr_risk = get_mr_risk_level()
    
    # Display header
    console.print("\n[bold blue]Repo Health Dashboard[/bold blue]")
    console.print("[blue]" + "="*25 + "[/blue]\n")
    
    # Display metrics with colors
    console.print(f"Security Score:     {get_colored_score(security_score)}/100")
    console.print(f"Doc Coverage:       {get_colored_score(doc_coverage)}%")
    console.print(f"Pipeline Status:    {get_colored_status(pipeline_status)}")
    console.print(f"MR Risk Level:      {get_colored_status(mr_risk)}")
    
    # Additional info
    console.print("\n[dim]Tip: Run 'glc scan', 'glc docs', and 'glc migrate' to improve health scores.[/dim]")