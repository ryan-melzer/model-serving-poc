#!/usr/bin/env python3
"""
Installation verification script for model-serving-poc environment.
"""

import sys
import shutil
from importlib.metadata import version

def check_system_packages():
    print("🔍 Checking system packages...")
    
    required_packages = ["kind", "kubectl", "helm", "istioctl", "jq", "k9s", "hey", "hatch", "uv"]
    missing_packages = []
    
    for package in required_packages:
        if shutil.which(package):
            print(f"✅ {package} - found")
        else:
            print(f"❌ {package} - not found")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: brew install " + " ".join(missing_packages))
        return False
    
    print("✅ All system packages are installed!")
    return True

def check_python_packages():
    print("\n🔍 Checking Python packages...")
    
    try:
        import mlflow
        import bentoml
        import xgboost
        import umami
        import sklearn
        print("✅ All Python packages are installed!")
        
        print(f"\n🔍 Checking umami version...")
        expected_umami_version = "0.0.56"
        try:
            actual_umami_version = version("umami")
            if actual_umami_version == expected_umami_version:
                print(f"✅ umami version {actual_umami_version} (expected: {expected_umami_version})")
            else:
                print(f"❌ umami version mismatch: found {actual_umami_version}, expected {expected_umami_version}")
                print("Please ensure you have the correct umami version installed.")
                return False
        except Exception as e:
            print(f"❌ Could not determine umami version: {e}")
            print("Please verify umami installation manually.")
            return False
            
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running this from within the hatch shell.")
        return False

def verify_installation():
    print("\n🔍 Verifying installation...")
    print("-" * 50)
    
    system_ok = check_system_packages()
    python_ok = check_python_packages()
    
    if system_ok and python_ok:
        print("\n🎉 Installation verification successful!")
        print("Your environment is ready to use.\n")
    else:
        print("\n❌ Installation verification failed!")
        print("Please fix the issues above and try again.\n")
        sys.exit(1)

if __name__ == "__main__":
    verify_installation()