from typing import List, Dict
from pydantic import BaseModel
import openai
from dotenv import load_dotenv

load_dotenv()

class Goal(BaseModel):
    text: str
    priority: int
    dependencies: List[str] = []

class Plan(BaseModel):
    goals: List[Goal]
    total_steps: int

def create_outline(topic: str) -> Plan:
    """Generate a structured outline for the given topic."""
    prompt = f"""
    Create a detailed outline for the topic: {topic}
    Break it down into specific, actionable goals.
    Each goal should be a single sentence and have a priority (1-5).
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a content planning expert."},
            {"role": "user", "content": prompt}
        ]
    )
    
    # Parse the response into goals
    goals = []
    for i, line in enumerate(response.choices[0].message.content.split('\n')):
        if line.strip():
            goals.append(Goal(
                text=line.strip(),
                priority=min(5, max(1, i % 5 + 1))  # Simple priority assignment
            ))
    
    return Plan(goals=goals, total_steps=len(goals))

def get_next_goal(plan: Plan, completed_goals: List[str]) -> Goal:
    """Get the next goal to work on based on priorities and dependencies."""
    available_goals = [
        goal for goal in plan.goals 
        if goal.text not in completed_goals
    ]
    
    if not available_goals:
        return None
        
    return max(available_goals, key=lambda g: g.priority) 