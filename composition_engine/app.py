import os
import json
import boto3
from dotenv import load_dotenv
from planner import create_outline, get_next_goal
from composer import generate_content, refine_content

# Load environment variables
load_dotenv()

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.getenv('DYNAMODB_TABLE', 'composemind-data'))

def store_trace(trace_id: str, step: int, goal: str, content: str):
    """Store a reasoning trace in DynamoDB."""
    item = {
        'id': f"{trace_id}-{step}",
        'trace_id': trace_id,
        'step': step,
        'goal': goal,
        'content': content,
        'type': 'trace'
    }
    table.put_item(Item=item)

def compose_content(topic: str, trace_id: str) -> dict:
    """Compose content for a given topic using step-by-step reasoning."""
    # Create outline
    plan = create_outline(topic)
    completed_goals = []
    context = {}
    
    # Process each goal
    for step in range(plan.total_steps):
        # Get next goal
        goal = get_next_goal(plan, completed_goals)
        if not goal:
            break
            
        # Generate content
        content = generate_content(goal, context)
        
        # Refine content
        refined_content = refine_content(content)
        
        # Store trace
        store_trace(trace_id, step + 1, goal.text, refined_content)
        
        # Update context and completed goals
        context['previous_content'] = refined_content
        completed_goals.append(goal.text)
    
    return {
        'trace_id': trace_id,
        'total_steps': len(completed_goals),
        'status': 'success'
    }

if __name__ == '__main__':
    # Example usage
    topic = "The benefits of cloud computing"
    trace_id = "sample-trace-1"
    
    result = compose_content(topic, trace_id)
    print(json.dumps(result, indent=2)) 