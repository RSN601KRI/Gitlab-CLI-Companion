import streamlit as st
import subprocess
import os

# Set page config
st.set_page_config(
    page_title="GitLab DevOps Companion Dashboard",
    page_icon="🚀",
    layout="wide"
)

# Title
st.title("🚀 GitLab DevOps Companion Dashboard")

# Description
st.markdown("""
Welcome to the GitLab DevOps Companion Dashboard. 
Use the controls below to run various DevOps automation commands.
""")

# Section: DevOps Automation Controls
st.header("⚙️ DevOps Automation Controls")

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

def run_command(cmd):
    """Run a glc command and return the output."""
    try:
        # Ensure we're in the correct directory (project root)
        project_root = os.path.dirname(os.path.abspath(__file__))
        os.chdir(project_root)
        
        # Run the command
        result = subprocess.run(['glc', cmd], 
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
        return "Error: 'glc' command not found. Make sure it's installed."
    except Exception as e:
        return f"Error running command: {str(e)}"

# Buttons
with col1:
    if st.button("🔄 Migrate", help=commands["migrate"]):
        with st.spinner("Running migration..."):
            st.session_state.output = run_command("migrate")

with col2:
    if st.button("📚 Docs", help=commands["docs"]):
        with st.spinner("Generating documentation..."):
            st.session_state.output = run_command("docs")

with col3:
    if st.button("🔍 Scan", help=commands["scan"]):
        with st.spinner("Running security scan..."):
            st.session_state.output = run_command("scan")

with col4:
    if st.button("❤️ Health", help=commands["health"]):
        with st.spinner("Checking repository health..."):
            st.session_state.output = run_command("health")

with col5:
    if st.button("🔎 Review", help=commands["review"]):
        with st.spinner("Analyzing MR risk..."):
            st.session_state.output = run_command("review")

# Output section
st.header("📋 Command Output")

if st.session_state.output:
    st.code(st.session_state.output, language="text")
else:
    st.info("Click a button above to run a command and see the output here.")

# Footer
st.markdown("---")
st.markdown("""
**GitLab DevOps Companion CLI** - Automate your DevOps workflows with ease!

For more information, see the [README](README.md).
""")

# Add some styling
st.markdown("""
<style>
    .stButton button {
        width: 100%;
        height: 60px;
        font-size: 16px;
    }
    .stCode {
        font-family: 'Courier New', monospace;
        white-space: pre-wrap;
    }
</style>
""", unsafe_allow_html=True)