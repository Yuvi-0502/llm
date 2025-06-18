#!/usr/bin/env python3
"""
Simple test to verify the modular client structure
"""

def test_imports():
    """Test that all client modules can be imported successfully"""
    try:
        from client.base_client import BaseClient
        from client.auth_client import AuthClient
        from client.news_client import NewsClient
        from client.notification_client import NotificationClient
        from client.admin_client import AdminClient
        from client.user_client import UserClient
        from client.main_client import NewsAggregatorClient
        
        print("✅ All client modules imported successfully!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_client_instantiation():
    """Test that the main client can be instantiated"""
    try:
        from client.main_client import NewsAggregatorClient
        client = NewsAggregatorClient()
        print("✅ Main client instantiated successfully!")
        return True
    except Exception as e:
        print(f"❌ Client instantiation error: {e}")
        return False

def test_base_functionality():
    """Test basic client functionality"""
    try:
        from client.base_client import BaseClient
        client = BaseClient()
        
        # Test email validation
        assert client.validate_email("test@example.com") == True
        assert client.validate_email("invalid-email") == False
        
        print("✅ Base client functionality works!")
        return True
    except Exception as e:
        print(f"❌ Base functionality error: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing modular client structure...\n")
    
    tests = [
        ("Import Test", test_imports),
        ("Instantiation Test", test_client_instantiation),
        ("Base Functionality Test", test_base_functionality)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        if test_func():
            passed += 1
        print()
    
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Modular client structure is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main() 