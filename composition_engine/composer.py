from typing import Dict, List
import openai
from dotenv import load_dotenv
from .planner import Goal

load_dotenv()

def generate_content(goal: Goal, context: Dict[str, str] = None) -> str:
    """Generate content for a specific goal."""
    prompt = f"""
    Goal: {goal.text}
    
    Previous context:
    {context.get('previous_content', 'No previous content')}
    
    Generate detailed content that addresses this goal.
    Focus on clarity and coherence.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a content generation expert."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content.strip()

def refine_content(content: str, feedback: str = None) -> str:
    """Refine the generated content based on feedback."""
    if not feedback:
        return content
        
    prompt = f"""
    Original content:
    {content}
    
    Feedback for improvement:
    {feedback}
    
    Please refine the content based on the feedback.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a content refinement expert."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content.strip() 