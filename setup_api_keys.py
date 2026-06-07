#!/usr/bin/env python3
"""
Enhanced API Key Setup Script
Supports multiple AI services and data sources
"""

import os
from dotenv import load_dotenv

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")


def print_info(text):
    """Print info text"""
    print(f"ℹ️  {text}")


def print_success(text):
    """Print success message"""
    print(f"✓ {text}")


def print_warning(text):
    """Print warning message"""
    print(f"⚠️  {text}")


def prompt_key(prompt_text, existing=None, required=False):
    """
    Prompt user for a key with optional existing value
    """
    display_text = prompt_text
    if existing:
        display_text += f" (Current: {existing[:10]}...)"
    display_text += ": "
    
    val = input(display_text).strip()
    
    if val:
        return val
    elif existing:
        return existing
    elif required:
        print_warning("This key is recommended. Skipping...")
        return None
    return None


def get_api_option():
    """Display API options and get user choice"""
    print_header("🔑 AI/API Service Options")
    
    print("Which AI service do you want to use for news analysis?\n")
    
    options = {
        "1": {
            "name": "OpenAI (GPT-3.5/GPT-4)",
            "key": "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",
            "url": "https://platform.openai.com/api-keys",
            "cost": "Paid - $0.0005 per 1K tokens (fastest)"
        },
        "2": {
            "name": "HuggingFace (Free models)",
            "key": "HUGGINGFACE_API_KEY",
            "url": "https://huggingface.co/settings/tokens",
            "cost": "Free - Rate limited"
        },
        "3": {
            "name": "Cohere API",
            "key": "COHERE_API_KEY",
            "url": "https://dashboard.cohere.ai/api-keys",
            "cost": "Free tier available - Good for text classification"
        },
        "4": {
            "name": "Google (PaLM/Gemini)",
            "key": "GOOGLE_API_KEY",
            "url": "https://makersuite.google.com/app/apikey",
            "cost": "Free tier - Limited requests"
        },
        "5": {
            "name": "All services (setup all APIs)",
            "key": "MULTIPLE",
            "url": "Multiple",
            "cost": "Mixed"
        }
    }
    
    for key, info in options.items():
        print(f"  {key}. {info['name']}")
        print(f"     Cost: {info['cost']}")
        print()
    
    choice = input("Enter your choice (1-5): ").strip()
    
    if choice in options:
        return choice, options
    else:
        print_warning("Invalid choice. Defaulting to OpenAI...")
        return "1", options


def setup_openai(existing):
    """Setup OpenAI API key"""
    print_info("OpenAI - https://platform.openai.com/api-keys")
    print_info("Models: gpt-3.5-turbo, gpt-4, gpt-4-turbo")
    print()
    
    key = prompt_key("Enter OpenAI API Key (sk-...)", existing.get("OPENAI_API_KEY"))
    
    if key:
        return {"OPENAI_API_KEY": key}
    return {}


def setup_huggingface(existing):
    """Setup HuggingFace API key"""
    print_info("HuggingFace - https://huggingface.co/settings/tokens")
    print_info("Free & Paid models available on HuggingFace Hub")
    print()
    
    key = prompt_key("Enter HuggingFace API Token (hf_...)", existing.get("HUGGINGFACE_API_KEY"))
    
    if key:
        return {"HUGGINGFACE_API_KEY": key}
    return {}


def setup_cohere(existing):
    """Setup Cohere API key"""
    print_info("Cohere - https://dashboard.cohere.ai/api-keys")
    print_info("Free tier: 100 API calls per minute, includes text classification")
    print()
    
    key = prompt_key("Enter Cohere API Key", existing.get("COHERE_API_KEY"))
    
    if key:
        return {"COHERE_API_KEY": key}
    return {}


def setup_google(existing):
    """Setup Google API key"""
    print_info("Google - https://makersuite.google.com/app/apikey")
    print_info("Models: palm, gemini-pro")
    print()
    
    key = prompt_key("Enter Google API Key", existing.get("GOOGLE_API_KEY"))
    
    if key:
        return {"GOOGLE_API_KEY": key}
    return {}


def setup_data_sources(existing):
    """Setup optional data source APIs"""
    print_header("📰 Optional: Data Source APIs")
    
    print("Do you want to setup data source APIs? (y/n): ", end="")
    if input().strip().lower() != 'y':
        return {}
    
    updates = {}
    
    # NewsAPI
    print_info("NewsAPI - Real news from 40K+ sources globally")
    print_info("Website: https://newsapi.org/")
    key = prompt_key("Enter NewsAPI Key (or leave blank)", existing.get("NEWSAPI_API_KEY"))
    if key:
        updates["NEWSAPI_API_KEY"] = key
    
    # Guardian API
    print_info("\nGuardian Open Platform - UK news articles")
    print_info("Website: https://open-platform.theguardian.com/")
    key = prompt_key("Enter Guardian API Key (or leave blank)", existing.get("GUARDIAN_API_KEY"))
    if key:
        updates["GUARDIAN_API_KEY"] = key
    
    return updates


def main():
    """Main setup function"""
    print_header("🚀 AI-Powered News Detector - API Key Setup")
    
    # Load existing .env
    load_dotenv()
    env_path = ".env"
    
    existing = {}
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.strip().split("=", 1)
                    existing[k] = v
        print_success(f"Found existing .env file with {len(existing)} keys")
    
    # Get API choice
    choice, options = get_api_option()
    
    updates = {}
    
    if choice == "5":
        # Setup all services
        print_header("Setting up all AI services")
        updates.update(setup_openai(existing))
        updates.update(setup_huggingface(existing))
        updates.update(setup_cohere(existing))
        updates.update(setup_google(existing))
    else:
        # Setup selected service
        selected = options[choice]
        print_header(f"Setting up {selected['name']}")
        
        if choice == "1":
            updates.update(setup_openai(existing))
        elif choice == "2":
            updates.update(setup_huggingface(existing))
        elif choice == "3":
            updates.update(setup_cohere(existing))
        elif choice == "4":
            updates.update(setup_google(existing))
    
    # Setup optional data sources
    updates.update(setup_data_sources(existing))
    
    # Merge with existing
    existing.update(updates)
    
    # Write to .env
    with open(env_path, "w") as f:
        f.write("# AI-Powered News Detector - API Keys\n")
        f.write("# DO NOT SHARE THIS FILE!\n\n")
        
        for k, v in existing.items():
            if v:  # Only write if value exists
                f.write(f"{k}={v}\n")
    
    print_header("✅ Setup Complete!")
    print_success(f".env file updated: {os.path.abspath(env_path)}")
    print(f"\nConfigured keys:")
    for k in updates.keys():
        print(f"  ✓ {k}")
    
    print_info("Next steps:")
    print("  1. Run: python fetch_news_multi.py")
    print("  2. Run: python train_model.py")
    print("  3. Run: python app.py")
    print()


if __name__ == "__main__":
    main()
