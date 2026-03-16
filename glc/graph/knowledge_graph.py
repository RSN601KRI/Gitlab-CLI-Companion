# Knowledge graph utilities using NetworkX
import networkx as nx
import json
import os

GRAPH_FILE = 'graph.json'

class KnowledgeGraph:
    """
    Knowledge graph for storing relationships between repository entities.
    
    Entities: files, pipelines, jobs, services, documentation
    Relationships: file -> pipeline, pipeline -> job, job -> script, file -> documentation
    """
    
    def __init__(self):
        self.graph = nx.DiGraph()
        # Add root repository node
        self.graph.add_node('repository', type='repository', label='Repository')
        self.load_graph()
    
    def load_graph(self):
        """Load graph from JSON file if it exists."""
        if os.path.exists(GRAPH_FILE):
            try:
                with open(GRAPH_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.graph = nx.node_link_graph(data, edges="links")
            except Exception as e:
                print(f"Error loading graph: {e}")
                self.graph = nx.DiGraph()
    
    def save_graph(self):
        """Save graph to JSON file."""
        try:
            data = nx.node_link_data(self.graph, edges="links")
            with open(GRAPH_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving graph: {e}")
    
    def add_file(self, file_path, file_type='file'):
        """Add a file node to the graph."""
        self.graph.add_node(file_path, type=file_type, label=os.path.basename(file_path))
    
    def add_pipeline(self, pipeline_name, pipeline_type='gitlab_ci'):
        """Add a pipeline node to the graph."""
        self.graph.add_node(f"pipeline:{pipeline_name}", type='pipeline', label=pipeline_name)
    
    def add_job(self, job_name, stage='unknown'):
        """Add a job node to the graph."""
        self.graph.add_node(f"job:{job_name}", type='job', label=job_name, stage=stage)
    
    def add_service(self, service_name, service_type='unknown'):
        """Add a service node to the graph."""
        self.graph.add_node(f"service:{service_name}", type='service', label=service_name)
    
    def add_documentation(self, doc_name, doc_type='markdown'):
        """Add a documentation node to the graph."""
        self.graph.add_node(f"doc:{doc_name}", type='documentation', label=doc_name)
    
    def add_relationship(self, source, target, relationship_type='related_to'):
        """Add an edge between two nodes."""
        self.graph.add_edge(source, target, type=relationship_type)
    
    def get_related_nodes(self, node, relationship_type=None):
        """Get nodes related to the given node."""
        if relationship_type:
            return [n for n in self.graph.neighbors(node) 
                   if self.graph[node][n].get('type') == relationship_type]
        return list(self.graph.neighbors(node))
    
    def get_node_info(self, node):
        """Get information about a node."""
        if node in self.graph:
            return dict(self.graph.nodes[node])
        return None
    
    def get_all_nodes_by_type(self, node_type):
        """Get all nodes of a specific type."""
        return [n for n, attrs in self.graph.nodes(data=True) 
               if attrs.get('type') == node_type]

# Global graph instance
kg = KnowledgeGraph()

def update_graph_from_migrate(jenkinsfile_path, gitlab_ci_path, stages):
    """
    Update knowledge graph after migration.
    
    Adds relationships: Jenkinsfile -> GitLab CI pipeline -> jobs
    """
    # Add file nodes
    kg.add_file(jenkinsfile_path, 'jenkinsfile')
    kg.add_file(gitlab_ci_path, 'gitlab_ci')
    
    # Add pipeline
    pipeline_name = 'gitlab_ci_pipeline'
    kg.add_pipeline(pipeline_name)
    
    # Connect Jenkinsfile to pipeline
    kg.add_relationship(jenkinsfile_path, f"pipeline:{pipeline_name}", 'migrates_to')
    
    # Add jobs and connect
    for stage in stages:
        job_name = stage.lower().replace(' ', '_')
        kg.add_job(job_name, stage.lower())
        kg.add_relationship(f"pipeline:{pipeline_name}", f"job:{job_name}", 'contains')
    
    kg.save_graph()

def update_graph_from_docs(files_generated):
    """
    Update knowledge graph after documentation generation.
    
    Adds documentation nodes and connects to files.
    """
    for doc_file in files_generated:
        kg.add_file(doc_file, 'documentation')
        # Connect repository to documentation
        kg.add_relationship('repository', doc_file, 'has_documentation')
    
    kg.save_graph()

def update_graph_from_scan(scan_results):
    """
    Update knowledge graph after security scan.
    
    Adds security findings as nodes.
    """
    for finding in scan_results:
        issue_node = f"issue:{finding['file']}:{finding['line']}"
        kg.graph.add_node(issue_node, 
                         type='security_issue', 
                         file=finding['file'], 
                         line=finding['line'], 
                         issue=finding['issue'], 
                         severity=finding['severity'])
        kg.add_relationship(finding['file'], issue_node, 'has_issue')
    
    kg.save_graph()