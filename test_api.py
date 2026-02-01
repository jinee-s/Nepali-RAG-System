"""
Test script for Nepali RAG Flask API
Run this after starting the Flask server to test all endpoints
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def print_separator():
    print("\n" + "="*60 + "\n")

def test_health():
    """Test health check endpoint"""
    print("🔍 Testing Health Check Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        data = response.json()
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_ask_question(question):
    """Test the main RAG endpoint"""
    print(f"💬 Testing Ask Question Endpoint...")
    print(f"Question: {question}")
    try:
        response = requests.post(
            f"{BASE_URL}/api/ask",
            json={"question": question, "top_k": 5},
            timeout=30
        )
        data = response.json()
        print(f"Status Code: {response.status_code}")
        print(f"\n📝 Answer: {data.get('answer', 'N/A')}")
        print(f"\n📊 Scores: {data.get('scores', [])}")
        print(f"\n📚 Context (first 200 chars): {data.get('context', '')[:200]}...")
        return response.status_code == 200 and data.get('success')
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_retrieve_only(query):
    """Test the retrieve-only endpoint"""
    print(f"🔎 Testing Retrieve Endpoint...")
    print(f"Query: {query}")
    try:
        response = requests.post(
            f"{BASE_URL}/api/retrieve",
            json={"query": query, "top_k": 3},
            timeout=30
        )
        data = response.json()
        print(f"Status Code: {response.status_code}")
        print(f"\n📄 Retrieved {data.get('count', 0)} documents")
        print(f"📊 Scores: {data.get('scores', [])}")
        if data.get('documents'):
            print(f"\n📝 First document: {data['documents'][0][:150]}...")
        return response.status_code == 200 and data.get('success')
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Nepali RAG System API Tests\n")
    print(f"Testing server at: {BASE_URL}")
    print_separator()
    
    # Test questions
    test_questions = [
        "नेपालको राजधानी के हो?",
        "नेपालमा कति वटा प्रदेश छन्?",
        "सगरमाथाको उचाइ कति छ?"
    ]
    
    results = []
    
    # 1. Test health endpoint
    print_separator()
    results.append(("Health Check", test_health()))
    
    time.sleep(1)
    
    # 2. Test ask question endpoint
    for question in test_questions:
        print_separator()
        results.append((f"Ask: {question}", test_ask_question(question)))
        time.sleep(2)  # Avoid rate limiting
    
    # 3. Test retrieve endpoint
    print_separator()
    results.append(("Retrieve", test_retrieve_only("नेपाल")))
    
    # Summary
    print_separator()
    print("📊 TEST SUMMARY")
    print_separator()
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    print(f"\nTotal: {passed}/{total} tests passed")
    print_separator()

if __name__ == "__main__":
    print("\n⚠️  Make sure the Flask server is running before executing tests!")
    print("   Run: python app.py\n")
    input("Press Enter to continue...")
    main()
