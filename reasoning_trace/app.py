import os
import json
from datetime import datetime
from dotenv import load_dotenv
from tracer import TraceLogger, TraceStep
from visualizer import TraceVisualizer

# Load environment variables
load_dotenv()

def process_trace(trace_id: str) -> dict:
    """Process a reasoning trace and generate visualizations."""
    # Initialize components
    logger = TraceLogger()
    visualizer = TraceVisualizer()
    
    # Get the trace
    trace = logger.get_trace(trace_id)
    if not trace:
        return {
            'error': f'Trace {trace_id} not found',
            'status': 'error'
        }
    
    # Generate visualizations
    mermaid_graph = visualizer.to_mermaid(trace)
    json_graph = visualizer.to_json(trace)
    
    return {
        'trace_id': trace_id,
        'mermaid': mermaid_graph,
        'graph': json_graph,
        'status': 'success'
    }

if __name__ == '__main__':
    # Example usage
    trace_id = "sample-trace-1"
    
    # Create a sample trace
    logger = TraceLogger()
    step = TraceStep(
        step_id="1",
        goal="Define cloud computing",
        content="Cloud computing is the delivery of computing services over the internet.",
        timestamp=datetime.utcnow().isoformat(),
        metadata={'dependencies': []}
    )
    logger.log_step(trace_id, step)
    
    # Process the trace
    result = process_trace(trace_id)
    print(json.dumps(result, indent=2)) 