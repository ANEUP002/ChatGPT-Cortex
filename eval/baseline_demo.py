"""
Demo Baseline Evaluation - Uses mock responses instead of OpenAI API
Perfect for testing without API credits
"""

from typing import List, Dict
import json
import time


class BaselineEvaluatorDemo:
    """
    Demo version - simulates ChatGPT WITHOUT memory
    """
    
    def chat(self, message: str) -> str:
        """
        Simulate ChatGPT response without memory
        """
        time.sleep(0.5)  # Simulate API delay
        
        message_lower = message.lower()
        
        # Simulate responses for different types of questions
        if "my name is" in message_lower:
            return "Nice to meet you! How can I help you today?"
        
        elif "cat named" in message_lower:
            return "That's wonderful! Cats make great companions."
        
        elif "favorite color" in message_lower and "is" in message_lower:
            return "That's a lovely color choice!"
        
        elif "work as" in message_lower or "software engineer" in message_lower:
            return "That sounds like an interesting job!"
        
        # Questions asking for recall (should fail without memory)
        elif "cat's name" in message_lower or "name of my cat" in message_lower:
            return "I'm sorry, I don't have information about your cat's name. Could you tell me?"
        
        elif "what's my favorite color" in message_lower or "my favorite color" in message_lower:
            return "I don't know your favorite color. What is it?"
        
        elif "where do i work" in message_lower:
            return "I don't have that information. Where do you work?"
        
        return "I understand. How can I assist you?"
    
    def run_test_scenario(self, test_questions: List[Dict]) -> Dict:
        """
        Run test scenario with simulated responses
        """
        results = {
            "total_questions": len(test_questions),
            "correct": 0,
            "responses": []
        }
        
        print("\n" + "="*50)
        print("BASELINE DEMO TEST (NO MEMORY)")
        print("="*50)
        
        for i, test in enumerate(test_questions, 1):
            print(f"\nQuestion {i}: {test['question']}")
            
            response = self.chat(test['question'])
            print(f"Response: {response}\n")
            
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
        """Check if response contains expected information"""
        response_lower = response.lower()
        
        for info in expected_info:
            if info.lower() in response_lower:
                return True
        return False


def create_test_questions() -> List[Dict]:
    """Create test questions that require memory"""
    return [
        {
            "context": "User introduces themselves",
            "question": "My name is Alex and I have a cat named Whiskers",
            "expected_info": ["nice", "meet", "wonderful", "great"]
        },
        {
            "context": "Ask about previously shared info",
            "question": "What is my cat's name?",
            "expected_info": ["don't know", "don't have", "sorry"]
        },
        {
            "context": "User shares favorite color",
            "question": "My favorite color is blue",
            "expected_info": ["lovely", "color"]
        },
        {
            "context": "Ask about favorite color",
            "question": "What's my favorite color?",
            "expected_info": ["don't know", "don't have"]
        },
        {
            "context": "User shares job",
            "question": "I work as a software engineer at Google",
            "expected_info": ["interesting", "sounds"]
        },
        {
            "context": "Ask about job",
            "question": "Where do I work?",
            "expected_info": ["don't have", "don't know"]
        }
    ]


if __name__ == "__main__":
    evaluator = BaselineEvaluatorDemo()
    test_questions = create_test_questions()
    results = evaluator.run_test_scenario(test_questions)
    
    with open("eval/baseline_results_demo.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("Results saved to eval/baseline_results_demo.json")