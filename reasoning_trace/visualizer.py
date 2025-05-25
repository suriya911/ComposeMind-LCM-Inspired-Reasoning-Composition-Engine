from typing import Dict, List
import networkx as nx
from .tracer import ReasoningTrace, TraceStep

class TraceVisualizer:
    def __init__(self):
        self.graph = nx.DiGraph()
    
    def _add_step_to_graph(self, step: TraceStep):
        """Add a step to the graph with its connections."""
        node_id = f"step_{step.step_id}"
        self.graph.add_node(
            node_id,
            label=step.goal,
            content=step.content
        )
        
        # Add edges based on step dependencies
        if 'dependencies' in step.metadata:
            for dep in step.metadata['dependencies']:
                self.graph.add_edge(f"step_{dep}", node_id)
    
    def create_graph(self, trace: ReasoningTrace) -> nx.DiGraph:
        """Create a graph from a reasoning trace."""
        self.graph.clear()
        
        # Add all steps to the graph
        for step in trace.steps:
            self._add_step_to_graph(step)
        
        return self.graph
    
    def to_mermaid(self, trace: ReasoningTrace) -> str:
        """Convert the trace to a Mermaid.js graph definition."""
        graph = self.create_graph(trace)
        
        # Start Mermaid diagram
        mermaid = ["graph TD"]
        
        # Add nodes
        for node in graph.nodes():
            node_data = graph.nodes[node]
            mermaid.append(f"    {node}[\"{node_data['label']}\"]")
        
        # Add edges
        for edge in graph.edges():
            mermaid.append(f"    {edge[0]} --> {edge[1]}")
        
        return "\n".join(mermaid)
    
    def to_json(self, trace: ReasoningTrace) -> Dict:
        """Convert the trace to a JSON structure for the frontend."""
        graph = self.create_graph(trace)
        
        nodes = []
        for node in graph.nodes():
            node_data = graph.nodes[node]
            nodes.append({
                'id': node,
                'label': node_data['label'],
                'content': node_data['content']
            })
        
        edges = []
        for edge in graph.edges():
            edges.append({
                'from': edge[0],
                'to': edge[1]
            })
        
        return {
            'nodes': nodes,
            'edges': edges,
            'metadata': {
                'trace_id': trace.trace_id,
                'created_at': trace.created_at,
                'updated_at': trace.updated_at
            }
        } 