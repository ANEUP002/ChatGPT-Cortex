from dotenv import load_dotenv
load_dotenv()


"""
Memory Evaluation - ChatGPT WITH Memory
Tests how well ChatGPT performs WITH the memory system
"""

import os
from typing import List, Dict
import json


class MemoryEvaluator:
    """
    Evaluates ChatGPT performance WITH memory system
    """
    
    def __init__(self):
        # TODO: This will connect to the actual memory graph once Person 1 completes it
        self.memory_graph = None
        
        # For now, simulate memory with a simple dict
        self.simulated_memory = {}
        
    def chat(self, message: str, user_id: str = "test_user") -> str:
        """
        Send a message and get response WITH memory
        """
        
        # TODO: Replace with actual graph call
        # response = self.memory_graph.invoke({"message": message, "user_id": user_id})
        
        # SIMULATION: Store facts in memory
        message_lower = message.lower()
        
        # Extract and store information
        if "my name is" in message_lower:
            name = message.split("my name is")[-1].split("and")[0].strip()
            self.simulated_memory["name"] = name
            return f"Nice to meet you, {name}! I'll remember that."
        
        elif "cat named" in message_lower:
            cat_name = message_lower.split("cat named")[-1].strip().rstrip(".")
            self.simulated_memory["cat_name"] = cat_name
            return f"Aww, {cat_name} sounds lovely! I'll remember your cat's name."
        
        elif "favorite color is" in message_lower:
            color = message_lower.split("favorite color is")[-1].strip().rstrip(".")
            self.simulated_memory["favorite_color"] = color
            return f"Got it! Your favorite color is {color}."
        
        elif "work as" in message_lower or "software engineer" in message_lower:
            if "google" in message_lower:
                self.simulated_memory["job"] = "software engineer at Google"
                return "Nice! Software engineer at Google - I'll remember that."
            else:
                job = message_lower.split("work as")[-1].strip().rstrip(".")
                self.simulated_memory["job"] = job
                return f"Cool! You work as {job}."
        
        # Answer recall questions
        elif "cat's name" in message_lower or "name of my cat" in message_lower:
            if "cat_name" in self.simulated_memory:
                return f"Your cat's name is {self.simulated_memory['cat_name'].title()}!"
            return "I don't think you've told me your cat's name yet."
        
        elif "favorite color" in message_lower:
            if "favorite_color" in self.simulated_memory:
                return f"Your favorite color is {self.simulated_memory['favorite_color']}!"
            return "I don't know your favorite color yet."
        
        elif "where do i work" in message_lower or "where i work" in message_lower:
            if "job" in self.simulated_memory:
                return f"You work as a {self.simulated_memory['job']}!"
            return "I don't think you've told me where you work yet."
        
        return "I understand. What else would you like to talk about?"
    
    def run_test_scenario(self, test_questions: List[Dict]) -> Dict:
        """
        Run a test scenario with memory
        """
        results = {
            "total_questions": len(test_questions),
            "correct": 0,
            "responses": []
        }
        
        print("\n" + "="*50)
        print("MEMORY TEST (WITH MEMORY)")
        print("="*50)
        
        for i, test in enumerate(test_questions, 1):
            print(f"\nQuestion {i}: {test['question']}")
            
            # Chat with memory enabled
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
        print(f"MEMORY RESULTS: {results['correct']}/{results['total_questions']} correct")
        print(f"Accuracy: {results['accuracy']*100:.1f}%")
        print("="*50 + "\n")
        
        return results
    
    def _check_answer(self, response: str, expected_info: List[str]) -> bool:
        """
        Check if response contains expected information
        """
        response_lower = response.lower()
        
        for info in expected_info:
            if info.lower() in response_lower:
                return True
        return False


# Use same test questions from baseline
from eval.baseline import create_test_questions


if __name__ == "__main__":
    # Run memory evaluation
    evaluator = MemoryEvaluator()
    test_questions = create_test_questions()
    results = evaluator.run_test_scenario(test_questions)
    
    # Save results
    with open("eval/memory_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("Results saved to eval/memory_results.json")