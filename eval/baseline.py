from dotenv import load_dotenv
load_dotenv()

"""
Baseline Evaluation - ChatGPT WITHOUT Memory
Tests how well ChatGPT performs without the memory system
"""

import os
from openai import OpenAI
from typing import List, Dict
import json


class BaselineEvaluator:
    """
    Evaluates ChatGPT performance WITHOUT memory
    """
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key) if api_key else None
        self.conversation_history = []
        
    def chat(self, message: str) -> str:
        """
        Send a message and get response (no memory between sessions)
        """
        if not self.client:
            return "Error: OPENAI_API_KEY not set"
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": message}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    def run_test_scenario(self, test_questions: List[Dict]) -> Dict:
        """
        Run a test scenario with multiple questions
        
        Args:
            test_questions: List of dicts with 'question', 'expected_info', 'context'
        
        Returns:
            Results dict with scores and responses
        """
        results = {
            "total_questions": len(test_questions),
            "correct": 0,
            "responses": []
        }
        
        print("\n" + "="*50)
        print("BASELINE TEST (NO MEMORY)")
        print("="*50)
        
        for i, test in enumerate(test_questions, 1):
            print(f"\nQuestion {i}: {test['question']}")
            
            # Simulate NEW conversation (no memory of previous)
            response = self.chat(test['question'])
            print(f"Response: {response}\n")
            
            # Check if response contains expected information
            is_correct = self._check_answer(response, test['expected_info'])
            
            if is_correct:
                results["correct"] += 1
                print("✓ CORRECT - Found expected information")
            else:
                print("✗ INCORRECT - Missing expected information")
            
            results["responses"].append({
                "question": test['question'],
                "response": response,
                "expected": test['expected_info'],
                "correct": is_correct
            })
        
        results["accuracy"] = results["correct"] / results["total_questions"]
        
        print("\n" + "="*50)
        print(f"BASELINE RESULTS: {results['correct']}/{results['total_questions']} correct")
        print(f"Accuracy: {results['accuracy']*100:.1f}%")
        print("="*50 + "\n")
        
        return results
    
    def _check_answer(self, response: str, expected_info: List[str]) -> bool:
        """
        Check if response contains expected information
        Simple string matching for now
        """
        response_lower = response.lower()
        
        # Check if ANY of the expected info is in the response
        for info in expected_info:
            if info.lower() in response_lower:
                return True
        return False


def create_test_questions() -> List[Dict]:
    """
    Create test questions that require memory
    """
    return [
        {
            "context": "User introduces themselves",
            "question": "My name is Alex and I have a cat named Whiskers",
            "expected_info": ["acknowledge", "alex", "cat", "whiskers"]
        },
        {
            "context": "Ask about previously shared info",
            "question": "What is my cat's name?",
            "expected_info": ["whiskers", "don't know", "didn't tell", "not sure"]
            # Baseline should say "I don't know" since it has no memory
        },
        {
            "context": "User shares favorite color",
            "question": "My favorite color is blue",
            "expected_info": ["blue", "acknowledge"]
        },
        {
            "context": "Ask about favorite color",
            "question": "What's my favorite color?",
            "expected_info": ["don't know", "didn't mention", "not sure", "blue"]
            # Should fail without memory
        },
        {
            "context": "User shares job",
            "question": "I work as a software engineer at Google",
            "expected_info": ["software", "engineer", "google"]
        },
        {
            "context": "Ask about job",
            "question": "Where do I work?",
            "expected_info": ["don't know", "haven't told", "google"]
            # Should fail without memory
        }
    ]


if __name__ == "__main__":
    # Run baseline evaluation
    evaluator = BaselineEvaluator()
    test_questions = create_test_questions()
    results = evaluator.run_test_scenario(test_questions)
    
    # Save results
    with open("eval/baseline_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("Results saved to eval/baseline_results.json")