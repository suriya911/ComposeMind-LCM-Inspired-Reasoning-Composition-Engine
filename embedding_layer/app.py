import os
import json
import boto3
from sentence_transformers import SentenceTransformer
import nltk
from nltk.tokenize import sent_tokenize
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.getenv('DYNAMODB_TABLE', 'composemind-data'))

# Download NLTK data
nltk.download('punkt', quiet=True)

# Initialize the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def segment_text(text):
    """Split text into sentences."""
    return sent_tokenize(text)

def generate_embeddings(sentences):
    """Generate embeddings for a list of sentences."""
    return model.encode(sentences).tolist()

def store_embeddings(text_id, sentences, embeddings):
    """Store sentences and their embeddings in DynamoDB."""
    item = {
        'id': text_id,
        'sentences': sentences,
        'embeddings': embeddings,
        'type': 'embedding'
    }
    table.put_item(Item=item)

def process_text(text_id, text):
    """Process text: segment, embed, and store."""
    # Segment text into sentences
    sentences = segment_text(text)
    
    # Generate embeddings
    embeddings = generate_embeddings(sentences)
    
    # Store in DynamoDB
    store_embeddings(text_id, sentences, embeddings)
    
    return {
        'text_id': text_id,
        'sentence_count': len(sentences),
        'status': 'success'
    }

if __name__ == '__main__':
    # Example usage
    sample_text = """
    ComposeMind is a cloud-native reasoning engine. 
    It uses advanced language models for composition.
    The system provides visual reasoning traces.
    """
    
    result = process_text('sample-1', sample_text)
    print(json.dumps(result, indent=2)) 