"""
Compare demo baseline vs memory performance
"""

import json
import os


def load_results(filename: str) -> dict:
    """Load results from JSON file"""
    if not os.path.exists(filename):
        return None
    
    with open(filename, 'r') as f:
        return json.load(f)


def compare_results():
    """Compare baseline and memory demo results"""
    baseline = load_results("eval/baseline_results_demo.json")
    memory = load_results("eval/memory_results_demo.json")
    
    if not baseline or not memory:
        print("❌ Error: Run baseline_demo.py and with_memory_demo.py first!")
        return
    
    print("\n" + "="*60)
    print("DEMO COMPARISON REPORT: BASELINE vs MEMORY")
    print("="*60)
    
    print(f"\n📊 ACCURACY")
    print(f"  Baseline (No Memory):  {baseline['correct']}/{baseline['total_questions']} = {baseline['accuracy']*100:.1f}%")
    print(f"  With Memory:           {memory['correct']}/{memory['total_questions']} = {memory['accuracy']*100:.1f}%")
    
    improvement = (memory['accuracy'] - baseline['accuracy']) * 100
    print(f"\n  📈 Improvement: +{improvement:.1f}%")
    
    print(f"\n📝 DETAILED COMPARISON")
    print("-" * 60)
    
    for i in range(len(baseline['responses'])):
        b_resp = baseline['responses'][i]
        m_resp = memory['responses'][i]
        
        print(f"\nQ{i+1}: {b_resp['question']}")
        print(f"  Baseline: {'✓' if b_resp['correct'] else '✗'} {b_resp['response'][:60]}...")
        print(f"  Memory:   {'✓' if m_resp['correct'] else '✗'} {m_resp['response'][:60]}...")
    
    print("\n" + "="*60)
    print("CONCLUSION")
    print("="*60)
    
    if memory['accuracy'] > baseline['accuracy']:
        print(f"✅ Memory system IMPROVED performance by {improvement:.1f}%")
        print("   The memory-augmented system demonstrates better recall")
        print("   and contextual understanding across conversations.")
    else:
        print("❌ Memory system did not improve performance")
    
    print("\n📌 NOTE: This is a demo using simulated responses.")
    print("   Real implementation would use OpenAI API + vector database.")
    print("="*60 + "\n")


if __name__ == "__main__":
    compare_results()