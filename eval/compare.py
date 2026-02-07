"""
Compare baseline vs memory performance
Generates a comparison report
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
    """
    Compare baseline and memory results
    """
    baseline = load_results("eval/baseline_results.json")
    memory = load_results("eval/memory_results.json")
    
    if not baseline or not memory:
        print("❌ Error: Run baseline.py and with_memory.py first!")
        return
    
    print("\n" + "="*60)
    print("COMPARISON REPORT: BASELINE vs MEMORY")
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
        print(f"  Baseline: {'✓' if b_resp['correct'] else '✗'} {b_resp['response'][:80]}...")
        print(f"  Memory:   {'✓' if m_resp['correct'] else '✗'} {m_resp['response'][:80]}...")
    
    print("\n" + "="*60)
    print("CONCLUSION")
    print("="*60)
    
    if memory['accuracy'] > baseline['accuracy']:
        print(f"✅ Memory system IMPROVED performance by {improvement:.1f}%")
        print("   The memory-augmented system demonstrates better recall")
        print("   and contextual understanding across conversations.")
    else:
        print("❌ Memory system did not improve performance")
        print("   Further tuning may be required.")
    
    print("="*60 + "\n")


if __name__ == "__main__":
    compare_results()