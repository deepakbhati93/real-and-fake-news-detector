"""
Setup OpenAI API Key
"""

print("\n" + "="*60)
print("🔑 OpenAI API Key Setup")
print("="*60 + "\n")

print("1. Go to: https://platform.openai.com/api-keys")
print("2. Sign in with your account")
print("3. Click 'Create new secret key'")
print("4. Copy the key\n")

api_key = input("Paste your OpenAI API key here: ").strip()

if not api_key.startswith('sk-proj-'):
    print("❌ Invalid key format. Should start with 'sk-proj-'")
    exit(1)

# Update .env file
with open('.env', 'w') as f:
    f.write(f"# OpenAI API Configuration\n")
    f.write(f"OPENAI_API_KEY={api_key}\n")
    f.write(f"\n# NewsAPI Configuration (for later use)\n")
    f.write(f"NEWSAPI_KEY=\n")
    f.write(f"\n# Model Configuration\n")
    f.write(f"USE_OPENAI=true\n")
    f.write(f"MODEL_NAME=gpt-3.5-turbo\n")

print("\n✅ API key saved to .env file!")
print("\nNext steps:")
print("  python fetch_news_openai.py")
print("  python train_model_enhanced.py")
print("  python app.py")
