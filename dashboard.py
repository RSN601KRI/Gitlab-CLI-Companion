import streamlit as st
import subprocess
import os
import re
import sys   # ✅ ADD THIS

sys.path.append(os.path.abspath("."))

# Set page config
st.set_page_config(
    page_title="GitLab DevOps Companion",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

def run_command(cmd):
    """Run a glc command and return the output."""
    try:
        # Ensure we're in the correct directory (project root)
        project_root = os.path.dirname(os.path.abspath(__file__))
        os.chdir(project_root)
        
        # Run using module instead of CLI
        result = subprocess.run(['python', '-m', 'glc.main', cmd], 
                              capture_output=True, 
                              text=True, 
                              timeout=60)
        
        # Combine stdout and stderr
        output = result.stdout
        if result.stderr:
            output += "\n--- STDERR ---\n" + result.stderr
            
        return output
        
    except subprocess.TimeoutExpired:
        return f"Command '{cmd}' timed out after 60 seconds."
    except FileNotFoundError:
        return "Error: Python module not found. Ensure virtual environment is active."
    except Exception as e:
        return f"Error running command: {str(e)}"

def parse_health_output(output):
    """Parse glc health output and extract metrics."""
    metrics = {
        'Security Score': 'N/A',
        'Doc Coverage': 'N/A', 
        'Pipeline Status': 'N/A',
        'MR Risk Level': 'N/A'
    }
    
    lines = output.split('\n')
    for line in lines:
        line = line.strip()
        if 'Security Score:' in line:
            metrics['Security Score'] = line.split(':', 1)[1].strip()
        elif 'Doc Coverage:' in line:
            metrics['Doc Coverage'] = line.split(':', 1)[1].strip()
        elif 'Pipeline Status:' in line:
            metrics['Pipeline Status'] = line.split(':', 1)[1].strip()
        elif 'MR Risk Level:' in line:
            metrics['MR Risk Level'] = line.split(':', 1)[1].strip()
    
    return metrics

# Sidebar navigation
st.sidebar.title("GitLab DevOps Companion")
st.sidebar.markdown("---")

pages = ["Home", "Problem We Solve", "Features", "Use Cases", "DevOps Dashboard", "Documentation", "About"]
page = st.sidebar.selectbox("Navigation", pages)

# Main content based on selected page
if page == "Home":
    # Home Page
    st.title("GitLab DevOps Companion")
    st.subheader("AI-powered DevOps co-pilot for GitLab repositories")

    # Short product description
    st.markdown("""
    **GitLab DevOps Companion** is an intelligent CLI tool that automates common DevOps tasks,
    enhances security, and provides comprehensive repository health insights for GitLab projects.
    """)

    # Feature highlights in 3-column layout
    st.markdown("---")
    st.subheader("Key Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        ### Pipeline Migration
        Automatically convert Jenkins pipelines to GitLab CI/CD with intelligent parsing and job generation.
        """)

    with col2:
        st.markdown("""
        ### Security Scanning
        Detect hardcoded secrets, insecure configurations, and CI/CD vulnerabilities in your repositories.
        """)

    with col3:
        st.markdown("""
        ### Health Dashboard
        Real-time repository health monitoring with security scores, coverage metrics, and risk assessment.
        """)

    # Brief explanation of how the CLI works
    st.markdown("---")
    st.subheader("How It Works")
    st.markdown("""
    The GitLab DevOps Companion CLI provides a suite of commands to automate your DevOps workflows:

    - **`glc migrate`** - Convert Jenkins pipelines to GitLab CI
    - **`glc scan`** - Security scan for secrets and configurations
    - **`glc docs`** - Generate comprehensive documentation
    - **`glc health`** - Repository health dashboard
    - **`glc review`** - Analyze merge request risk

    Simply run commands in your terminal or use this web dashboard for an interactive experience.
    """)

elif page == "Problem We Solve":
    # Problem We Solve Page
    st.title("The Problems We Solve")

    st.markdown("""
    ### Common DevOps Challenges

    Modern DevOps teams face numerous challenges that slow down development and compromise security.
    """)

    # Problems list
    st.markdown("#### Current Challenges:")
    st.markdown("""
    - **Jenkins to GitLab migration is manual**: Converting pipelines requires extensive manual effort and expertise
    - **Documentation becomes outdated**: Repository docs quickly become stale and unmaintainable
    - **Secrets are accidentally committed**: Sensitive credentials and API keys end up in version control
    - **Large merge requests introduce hidden risks**: Big PRs can break production systems without proper review
    - **No unified repository health overview**: Teams lack comprehensive visibility into repository status
    """)

    st.markdown("---")

    # Solution section
    st.subheader("Our Solution")
    st.markdown("""
    GitLab DevOps Companion CLI automates these workflows with intelligent AI-powered tools:

    - **Intelligent Migration**: AI-powered Jenkins to GitLab CI conversion with zero manual intervention
    - **Auto-Documentation**: Automatically generates and maintains comprehensive project documentation
    - **Security First**: Automated secret detection and security scanning prevents credential exposure
    - **Risk Assessment**: Predicts merge request impact and identifies potential deployment risks
    - **Health Monitoring**: Provides unified repository health dashboard with actionable insights

    **Transform your DevOps workflow with intelligent automation.**
    """)

elif page == "Features":
    # Features Page
    st.title("Features")

    st.markdown("### Comprehensive DevOps Automation Suite")

    # Feature cards in columns
    col1, col2 = st.columns(2)

    with col1:
        # Migration Feature
        st.markdown("""
        <div style="border: 2px solid #e1e5e9; border-radius: 10px; padding: 20px; margin: 10px 0; background-color: #f8f9fa;">
            <h3 style="color: #ff6b35;"> glc migrate</h3>
            <p><strong>Converts Jenkins pipelines to GitLab CI</strong></p>
            <ul>
                <li>Automated pipeline conversion</li>
                <li>Preserves job logic and dependencies</li>
                <li>Generates optimized GitLab CI configuration</li>
                <li>Zero manual intervention required</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # Documentation Feature
        st.markdown("""
        <div style="border: 2px solid #e1e5e9; border-radius: 10px; padding: 20px; margin: 10px 0; background-color: #f8f9fa;">
            <h3 style="color: #4CAF50;"> glc docs</h3>
            <p><strong>Automatically generates README, CONTRIBUTING and architecture documentation</strong></p>
            <ul>
                <li>Analyzes repository structure</li>
                <li>Creates comprehensive documentation</li>
                <li>Generates architecture diagrams</li>
                <li>Keeps docs synchronized with code</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # Health Feature
        st.markdown("""
        <div style="border: 2px solid #e1e5e9; border-radius: 10px; padding: 20px; margin: 10px 0; background-color: #f8f9fa;">
            <h3 style="color: #2196F3;"> glc health</h3>
            <p><strong>Provides a repository health dashboard</strong></p>
            <ul>
                <li>Security score monitoring</li>
                <li>Documentation coverage metrics</li>
                <li>Pipeline validation status</li>
                <li>Merge request risk assessment</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Security Scan Feature
        st.markdown("""
        <div style="border: 2px solid #e1e5e9; border-radius: 10px; padding: 20px; margin: 10px 0; background-color: #f8f9fa;">
            <h3 style="color: #f44336;"> glc scan</h3>
            <p><strong>Scans the repository for secrets and insecure configurations</strong></p>
            <ul>
                <li>Detects hardcoded secrets</li>
                <li>Identifies insecure configurations</li>
                <li>Scans for API keys and tokens</li>
                <li>Provides detailed security reports</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # Review Feature
        st.markdown("""
        <div style="border: 2px solid #e1e5e9; border-radius: 10px; padding: 20px; margin: 10px 0; background-color: #f8f9fa;">
            <h3 style="color: #FF9800;"> glc review</h3>
            <p><strong>Analyzes code changes and predicts risk</strong></p>
            <ul>
                <li>Evaluates merge request impact</li>
                <li>Predicts deployment risks</li>
                <li>Suggests files for review</li>
                <li>Assesses blast radius of changes</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif page == "Use Cases":
    # Use Cases Page
    st.title("Use Cases")

    st.markdown("### How Different Teams Benefit")

    # DevOps Engineers
    st.subheader("For DevOps Engineers")
    st.markdown("""
    - **Automated Migrations**: Quickly migrate legacy Jenkins pipelines to GitLab CI
    - **Security Automation**: Continuous security scanning and compliance checks
    - **Health Monitoring**: Real-time visibility into pipeline and repository health
    - **Documentation**: Automated generation of deployment and architecture docs
    """)

    # Development Teams
    st.subheader("For Development Teams")
    st.markdown("""
    - **Risk Assessment**: Understand the impact of code changes before merging
    - **Security Awareness**: Early detection of security issues in development
    - **Documentation**: Always up-to-date project documentation
    - **CI/CD Insights**: Better understanding of pipeline configurations
    """)

    # Open Source Maintainers
    st.subheader("For Open Source Maintainers")
    st.markdown("""
    - **Contributor Onboarding**: Automated documentation generation
    - **Security Compliance**: Regular security scans for public repositories
    - **Health Monitoring**: Maintain repository quality and standards
    - **Migration Support**: Help contributors migrate from other CI systems
    """)

    # Security Teams
    st.subheader("For Security Teams")
    st.markdown("""
    - **Secret Detection**: Automated scanning for exposed credentials
    - **Risk Assessment**: Evaluate security impact of code changes
    - **Compliance Monitoring**: Ensure security best practices are followed
    - **Audit Trail**: Comprehensive security reports and metrics
    """)

elif page == "DevOps Dashboard":
    # DevOps Dashboard Page
    st.title("DevOps Dashboard")

    # Repository Health Overview
    st.header("Repository Health Overview")

    with st.spinner("Loading repository health..."):
        health_output = run_command("health")
        health_metrics = parse_health_output(health_output)

    # Display metrics in columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Security Score", health_metrics['Security Score'])

    with col2:
        st.metric("Doc Coverage", health_metrics['Doc Coverage'])

    with col3:
        st.metric("Pipeline Status", health_metrics['Pipeline Status'])

    with col4:
        st.metric("MR Risk Level", health_metrics['MR Risk Level'])

    # DevOps Automation Controls
    st.header("DevOps Automation Controls")

    # Create columns for buttons
    col1, col2, col3, col4, col5 = st.columns(5)

    commands = {
        "migrate": "Convert Jenkins to GitLab CI",
        "docs": "Generate Documentation",
        "scan": "Security Scan",
        "health": "Repository Health",
        "review": "MR Risk Analysis"
    }

    # Initialize session state for output
    if 'output' not in st.session_state:
        st.session_state.output = ""

    # Buttons
    with col1:
        if st.button("Migrate", help=commands["migrate"]):
            with st.spinner("Running migration..."):
                st.session_state.output = run_command("migrate")

    with col2:
        if st.button("Docs", help=commands["docs"]):
            with st.spinner("Generating documentation..."):
                st.session_state.output = run_command("docs")

    with col3:
        if st.button("Scan", help=commands["scan"]):
            with st.spinner("Running security scan..."):
                st.session_state.output = run_command("scan")

    with col4:
        if st.button("Health", help=commands["health"]):
            with st.spinner("Checking repository health..."):
                st.session_state.output = run_command("health")

    with col5:
        if st.button("Review", help=commands["review"]):
            with st.spinner("Analyzing MR risk..."):
                st.session_state.output = run_command("review")

    # Output section
    st.header("Command Output")

    if st.session_state.output:
        st.code(st.session_state.output, language="text")
    else:
        st.info("Click a button above to run a command and see the output here.")

elif page == "Documentation":
    # Documentation Page
    st.title("Documentation")

    st.header("Getting Started")

    st.subheader("Installation")
    st.code("""
# Clone the repository
git clone <repository-url>
cd gitlab-devops-companion

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Install the CLI
pip install -e .
    """, language="bash")

    st.subheader("Commands")
    st.markdown("""
    The GitLab DevOps Companion CLI provides the following commands:
    """)

    # Command details
    commands_data = [
        ("glc migrate", "Convert Jenkins pipelines to GitLab CI", "Automatically converts Jenkins pipeline configurations to GitLab CI/CD format"),
        ("glc docs", "Generate repository documentation", "Creates comprehensive README, CONTRIBUTING, and architecture documentation"),
        ("glc scan", "Security scan for secrets and configurations", "Scans the repository for hardcoded secrets, API keys, and insecure configurations"),
        ("glc health", "Repository health dashboard", "Provides comprehensive repository health metrics and insights"),
        ("glc review", "Analyze merge request risk", "Evaluates code changes and predicts deployment risks")
    ]

    for cmd, desc, details in commands_data:
        st.markdown(f"**`{cmd}`** - {desc}")
        st.markdown(f"*{details}*")
        st.markdown("")

    st.subheader("Example Workflow")
    st.code("""
# 1. Migrate from Jenkins to GitLab CI
glc migrate

# 2. Generate documentation
glc docs

# 3. Run security scan
glc scan

# 4. Check repository health
glc health

# 5. Review merge request risk
glc review
    """, language="bash")

    st.subheader("Command Examples")

    with st.expander("Migration Example"):
        st.code("""
$ glc migrate

Pipeline Migration Summary
--------------------------
Jenkins Stages Found: 3
GitLab Jobs Generated: 3
File Created: .gitlab-ci.yml

Migration completed successfully!
        """)

    with st.expander("Health Check Example"):
        st.code("""
$ glc health

Repository Health Dashboard
==========================

Security Score:     85/100
Doc Coverage:       90%
Pipeline Status:    Valid
MR Risk Level:      Low

Recommendations:
- Consider adding more documentation
- Review security scan results
        """)

elif page == "About":
    # About Page
    st.title("About")

    st.markdown("""
    ### GitLab DevOps Companion

    An intelligent CLI tool that automates DevOps workflows, enhances security,
    and provides comprehensive repository health insights using AI-powered automation.

    The GitLab DevOps Companion bridges the gap between development teams and DevOps excellence
    by providing automated solutions to common challenges in modern software development.
    """)

    st.header("Architecture Overview")

    st.markdown("""
    The system is built around a modular architecture with a knowledge graph at its core,
    enabling intelligent automation and comprehensive repository analysis.
    """)

    # Architecture diagram
    st.subheader("System Architecture")
    st.code("""
graph TD
    A[Developer] --> B[CLI Interface]
    B --> C[Knowledge Graph]
    C --> D[Migration Engine]
    C --> E[Security Scanner]
    C --> F[Documentation Generator]
    C --> G[MR Risk Analyzer]

    D --> H[GitLab CI Pipeline]
    E --> I[Security Report]
    F --> J[Documentation Files]
    G --> K[Risk Assessment]
    """, language="mermaid")

    st.header("Tech Stack")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Core Technologies:**
        - **Python** - Primary programming language
        - **Typer CLI** - Modern command-line interface framework
        - **Streamlit UI** - Interactive web dashboard
        - **GitLab CI/CD** - Continuous integration and deployment

        **Data & Intelligence:**
        - **Knowledge Graph** - Repository relationship modeling
        """)

    with col2:
        st.markdown("""
        **DevOps Engines:**
        - **Migration Engine** - Jenkins to GitLab CI conversion
        - **Security Scanner** - Secret detection and vulnerability analysis
        - **Documentation Generator** - Automated docs creation
        - **MR Risk Analyzer** - Merge request impact assessment

        **Integration & Tools:**
        - GitPython for repository operations
        - NetworkX for graph algorithms
        - Rich for terminal UI enhancements
        """)

    st.header("Future Roadmap")

    st.markdown("""
    **Phase 1 (Current) - Foundation:**
    - Core CLI tool with essential DevOps commands
    - Knowledge graph implementation for repository intelligence
    - Streamlit web dashboard for interactive operations
    - GitLab CI/CD integration and pipeline management

    **Phase 2 (Next) - Enhancement:**
    - Multi-repository support and cross-project analysis
    - Advanced AI analysis with machine learning predictions
    - Custom rule engines for organization-specific policies
    - Team collaboration features and shared dashboards
    - Integration with additional CI/CD platforms

    **Phase 3 (Future) - Intelligence:**
    - ML-powered deployment risk predictions
    - Auto-remediation for detected issues
    - Enterprise integrations and SSO support
    - Advanced security scanning with threat intelligence
    - Predictive analytics for development workflows
    """)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**GitLab DevOps Companion**")
st.sidebar.markdown("AI-powered DevOps automation")
st.sidebar.markdown("[📖 README](README.md) | [🐙 GitHub](https://github.com)")

# Add styling
st.markdown("""
<style>
    .stButton button {
        width: 100%;
        height: 60px;
        font-size: 16px;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)