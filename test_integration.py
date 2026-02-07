"""Quick integration test for the memory system."""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing GPTMemory Integration...")
print("=" * 50)

# Test 1: Embeddings
print("\n1. Testing db/embeddings.py...")
try:
    from db.embeddings import get_embeddings
    embeddings = get_embeddings()
    print("   ✓ get_embeddings() works")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 2: Vector Store
print("\n2. Testing db/vector_store.py...")
try:
    from db.vector_store import init_vector_store, add_documents, similarity_search
    store = init_vector_store()
    print("   ✓ init_vector_store() works")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 3: Memory Store
print("\n3. Testing memory/store.py...")
try:
    from memory.store import store_summary, store_memory
    print("   ✓ store_summary import works")
    print("   ✓ store_memory import works")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 4: Memory Retrieve
print("\n4. Testing memory/retrieve.py...")
try:
    from memory.retrieve import retrieve_memories, format_memories_for_prompt
    print("   ✓ retrieve_memories import works")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 5: Graph Pipeline
print("\n5. Testing graph/pipeline.py...")
try:
    from graph.pipeline import build_graph
    print("   ✓ build_graph import works")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 6: Full flow (requires OPENAI_API_KEY)
print("\n6. Testing full storage flow...")
try:
    doc_id = store_summary("Test memory: user likes Python", session_id="test-session")
    print(f"   ✓ Stored document: {doc_id[:20]}...")
    
    results = retrieve_memories("What languages does user like?", k=1)
    if results:
        print(f"   ✓ Retrieved: {results[0]['text'][:50]}...")
    else:
        print("   ✓ Retrieval works (no results yet)")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 50)
print("Integration test complete!")
