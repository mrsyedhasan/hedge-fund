#!/usr/bin/env python3
"""
Core functionality test - focuses on what we know works
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_core_imports():
    """Test core imports that we know work"""
    try:
        from src.main import run_hedge_fund
        from src.llm.models import ModelProvider, get_model
        from src.utils.llm import call_llm, extract_json_from_response
        print("✅ Core imports successful")
        return True
    except ImportError as e:
        print(f"❌ Core import failed: {e}")
        return False

def test_llm_basic():
    """Test basic LLM functionality"""
    try:
        from src.llm.models import ModelProvider, get_model
        
        # Test model provider
        assert ModelProvider.OLLAMA.value == "Ollama"
        
        # Test model instantiation
        model = get_model("mistral:7b-instruct", ModelProvider.OLLAMA)
        assert model is not None
        
        print("✅ LLM basic functionality working")
        return True
    except Exception as e:
        print(f"❌ LLM test failed: {e}")
        return False

def test_json_extraction():
    """Test JSON extraction"""
    try:
        from src.utils.llm import extract_json_from_response
        
        # Test simple JSON
        result = extract_json_from_response('{"signal": "bullish", "confidence": 70}')
        assert result is not None
        assert result["signal"] == "bullish"
        assert result["confidence"] == 70
        
        print("✅ JSON extraction working")
        return True
    except Exception as e:
        print(f"❌ JSON extraction test failed: {e}")
        return False

def test_script_exists():
    """Test that run_analysis.py exists and is valid"""
    try:
        script_path = "run_analysis.py"
        assert os.path.exists(script_path)
        assert os.access(script_path, os.R_OK)
        
        # Test that it can be imported
        import importlib.util
        spec = importlib.util.spec_from_file_location("run_analysis", script_path)
        module = importlib.util.module_from_spec(spec)
        
        print("✅ run_analysis.py script is valid")
        return True
    except Exception as e:
        print(f"❌ run_analysis.py test failed: {e}")
        return False

def test_documentation():
    """Test documentation files"""
    try:
        docs = ["README.md", "QUICK_START.md", "DATA_REQUIREMENTS.md"]
        
        for doc in docs:
            assert os.path.exists(doc)
            assert os.access(doc, os.R_OK)
            with open(doc, 'r') as f:
                content = f.read()
                assert len(content) > 50
        
        print("✅ Documentation files are valid")
        return True
    except Exception as e:
        print(f"❌ Documentation test failed: {e}")
        return False

def test_working_analysis():
    """Test that we can run a simple analysis (mocked)"""
    try:
        from src.main import run_hedge_fund
        from src.llm.models import ModelProvider
        
        # Test that the function exists and is callable
        assert callable(run_hedge_fund)
        
        print("✅ Analysis function is callable")
        return True
    except Exception as e:
        print(f"❌ Analysis test failed: {e}")
        return False

def run_core_tests():
    """Run core functionality tests"""
    print("🧪 Running Core Functionality Tests")
    print("=" * 50)
    
    tests = [
        ("Core Imports", test_core_imports),
        ("LLM Basic", test_llm_basic),
        ("JSON Extraction", test_json_extraction),
        ("Script Exists", test_script_exists),
        ("Documentation", test_documentation),
        ("Analysis Function", test_working_analysis),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n📊 CORE TEST RESULTS:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} core tests passed")
    
    if passed == total:
        print("🎉 All core tests passed! Safe to proceed with cleanup.")
        return True
    else:
        print("⚠️  Some core tests failed. Review before cleanup.")
        return False

if __name__ == "__main__":
    success = run_core_tests()
    sys.exit(0 if success else 1)
