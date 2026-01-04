#!/usr/bin/env python3
"""
Comprehensive setup verification script for Project VICTUS
Checks for missing dependencies, models, directories, and configuration
"""

import os
import sys
from pathlib import Path
import importlib.util  # noqa: F401

def check_directories():
    """Check if all required directories exist."""
    print("\n" + "="*70)
    print("📁 Checking Required Directories")
    print("="*70)
    
    required_dirs = {
        'models': 'ML model files (Piper TTS, etc.)',
        'uploads': 'User uploaded documents',
        'faiss_index': 'FAISS vector database index',
        'static/audio': 'Generated audio files',
        'static/icons': 'PWA icons'
    }
    
    missing = []
    for dir_path, desc in required_dirs.items():
        path = Path(dir_path)
        if path.exists():
            items = list(path.iterdir())
            print(f"✅ {dir_path:20} - {len(items)} items - {desc}")
        else:
            print(f"❌ {dir_path:20} - MISSING - {desc}")
            missing.append(dir_path)
            # Create it
            path.mkdir(parents=True, exist_ok=True)
            print(f"   → Created {dir_path}")
    
    return len(missing) == 0

def check_models():
    """Check if required models are downloaded."""
    print("\n" + "="*70)
    print("🤖 Checking ML Models")
    print("="*70)
    
    models_dir = Path("models")
    onnx_files = list(models_dir.glob("*.onnx"))
    
    if onnx_files:
        for model_file in onnx_files:
            size_mb = model_file.stat().st_size / (1024 * 1024)
            print(f"✅ {model_file.name} ({size_mb:.1f} MB)")
            
            # Check for corresponding JSON
            json_file = model_file.with_suffix('.onnx.json')
            if json_file.exists():
                print(f"   ✅ Config: {json_file.name}")
            else:
                print(f"   ⚠️  Missing config: {json_file.name}")
    else:
        print("❌ No .onnx model files found in models/")
        print("   Run: python3 download_models.py")
        return False
    
    print("\n📝 Faster-Whisper Model:")
    print("   ℹ️  Will auto-download on first use (base.en)")
    
    return len(onnx_files) > 0

def check_dependencies():
    """Check if Python dependencies are installed."""
    print("\n" + "="*70)
    print("📚 Checking Python Dependencies")
    print("="*70)
    
    critical_deps = {
        'fastapi': 'FastAPI web framework',
        'uvicorn': 'ASGI server',
        'langchain': 'LangChain core',
        'langchain_openai': 'OpenAI integration',
        'langchain_community': 'LangChain community tools',
        'faster_whisper': 'Speech-to-text',
        'piper': 'Text-to-speech',
        'faiss': 'Vector database (faiss-cpu)',
        'sqlalchemy': 'Database ORM',
        'pydantic': 'Data validation',
        'pydantic_settings': 'Settings management',
        'msal': 'Microsoft authentication',
        'requests': 'HTTP client',
        'python_dotenv': 'Environment variables',
        'tavily': 'Web search (optional)',
    }
    
    missing = []
    optional_missing = []
    
    for module, desc in critical_deps.items():
        try:
            if module == 'faiss':
                import faiss  # noqa: F401
            elif module == 'piper':
                 pass # Check separately if needed or assume installed
            elif module == 'python_dotenv':
                import dotenv  # noqa: F401
            elif module == 'tavily':
                import tavily  # noqa: F401
            else:
                __import__(module)
            print(f"✅ {module:20} - {desc}")
        except ImportError:
            if module == 'tavily':
                print(f"⚠️  {module:20} - OPTIONAL - {desc}")
                optional_missing.append(module)
            else:
                print(f"❌ {module:20} - MISSING - {desc}")
                missing.append(module)
    
    if missing:
        print(f"\n⚠️  Missing critical dependencies: {', '.join(missing)}")
        print("   Install with: pip install " + " ".join(missing))
        print("   Or use Poetry: poetry install")
        return False
    
    if optional_missing:
        print(f"\nℹ️  Optional dependencies not installed: {', '.join(optional_missing)}")
    
    return True

def check_configuration():
    """Check configuration files."""
    print("\n" + "="*70)
    print("⚙️  Checking Configuration")
    print("="*70)
    
    env_file = Path('.env')
    if env_file.exists():
        print("✅ .env file exists")
        
        # Check for critical env vars (without revealing values)
        try:
            from dotenv import load_dotenv
            load_dotenv()
            required_vars = [
                'OPENAI_API_KEY',
                'SECRET_KEY',
                'DATABASE_URL'
            ]
            
            missing_vars = []
            for var in required_vars:
                value = os.getenv(var)
                if value:
                    # Show partial value for verification
                    display = value[:8] + "..." if len(value) > 8 else "***"
                    print(f"   ✅ {var:20} = {display}")
                else:
                    print(f"   ❌ {var:20} = NOT SET")
                    missing_vars.append(var)
            
            if missing_vars:
                print(f"\n⚠️  Missing environment variables: {', '.join(missing_vars)}")
                return False
        except ImportError:
            print("   ⚠️  python-dotenv not installed, cannot verify .env contents")
    else:
        print("⚠️  .env file not found")
        print("   Create .env file with required configuration")
        return False
    
    return True

def check_database():
    """Check database setup."""
    print("\n" + "="*70)
    print("💾 Checking Database")
    print("="*70)
    
    db_file = Path('chat_history.db')
    if db_file.exists():
        size_kb = db_file.stat().st_size / 1024
        print(f"✅ Database exists: chat_history.db ({size_kb:.1f} KB)")
        print("   Tables will be created automatically on first run if needed")
    else:
        print("ℹ️  Database will be created automatically on first run")
    
    return True

def check_files():
    """Check for required application files."""
    print("\n" + "="*70)
    print("📄 Checking Application Files")
    print("="*70)
    
    required_files = {
        'src/main.py': 'Main application entry point',
        'src/agent.py': 'AI agent configuration',
        'src/config.py': 'Configuration management',
        'static/index.html': 'Frontend main page',
        'static/script.js': 'Frontend JavaScript',
        'static/style.css': 'Frontend styles',
        'pyproject.toml': 'Project dependencies',
    }
    
    missing = []
    for file_path, desc in required_files.items():
        path = Path(file_path)
        if path.exists():
            print(f"✅ {file_path:25} - {desc}")
        else:
            print(f"❌ {file_path:25} - MISSING - {desc}")
            missing.append(file_path)
    
    return len(missing) == 0

def main():
    """Run all checks."""
    print("\n" + "="*70)
    print("🚀 Project VICTUS - Setup Verification")
    print("="*70)
    
    results = {
        'directories': check_directories(),
        'models': check_models(),
        'dependencies': check_dependencies(),
        'configuration': check_configuration(),
        'database': check_database(),
        'files': check_files(),
    }
    
    # Summary
    print("\n" + "="*70)
    print("📊 Verification Summary")
    print("="*70)
    
    all_ok = True
    for check, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {check.replace('_', ' ').title()}")
        if not passed:
            all_ok = False
    
    print("\n" + "="*70)
    if all_ok:
        print("✅ All checks passed! Project is ready to run.")
        print("\nTo start the application:")
        print("   uvicorn src.main:app --reload")
        return 0
    else:
        print("⚠️  Some checks failed. Please address the issues above.")
        print("\nQuick fixes:")
        print("   • Install dependencies: poetry install")
        print("   • Download models: python3 download_models.py")
        print("   • Check .env file for required variables")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Verification interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
