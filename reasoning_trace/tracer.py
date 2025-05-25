from typing import Dict, List, Optional
from pydantic import BaseModel
import boto3
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class TraceStep(BaseModel):
    step_id: str
    goal: str
    content: str
    timestamp: str
    metadata: Dict = {}

class ReasoningTrace(BaseModel):
    trace_id: str
    steps: List[TraceStep]
    created_at: str
    updated_at: str

class TraceLogger:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(os.getenv('DYNAMODB_TABLE', 'composemind-data'))
    
    def log_step(self, trace_id: str, step: TraceStep):
        """Log a single reasoning step."""
        item = {
            'id': f"{trace_id}-{step.step_id}",
            'trace_id': trace_id,
            'step_id': step.step_id,
            'goal': step.goal,
            'content': step.content,
            'timestamp': step.timestamp,
            'metadata': step.metadata,
            'type': 'trace_step'
        }
        self.table.put_item(Item=item)
    
    def get_trace(self, trace_id: str) -> Optional[ReasoningTrace]:
        """Retrieve a complete reasoning trace."""
        response = self.table.query(
            KeyConditionExpression='trace_id = :tid',
            ExpressionAttributeValues={':tid': trace_id}
        )
        
        if not response['Items']:
            return None
            
        steps = []
        for item in response['Items']:
            if item['type'] == 'trace_step':
                steps.append(TraceStep(
                    step_id=item['step_id'],
                    goal=item['goal'],
                    content=item['content'],
                    timestamp=item['timestamp'],
                    metadata=item.get('metadata', {})
                ))
        
        return ReasoningTrace(
            trace_id=trace_id,
            steps=sorted(steps, key=lambda x: x.step_id),
            created_at=steps[0].timestamp if steps else datetime.utcnow().isoformat(),
            updated_at=steps[-1].timestamp if steps else datetime.utcnow().isoformat()
        ) 