import os
from dotenv import load_dotenv

"""Simple helper script to create or update the .env file with API keys.
Run this and follow the prompts. It will store values in .env and keep
existing keys unchanged unless you choose to overwrite.
"""

def prompt_key(name, existing=None):
    if existing:
        prompt = f"{name} already set to '{existing}'. Enter new value to overwrite or leave blank to keep: "
    else:
        prompt = f"Enter your {name}: "
    val = input(prompt).strip()
    if val:
        return val
    return existing


def main():
    load_dotenv()
    env_path = os.path.join(os.getcwd(), ".env")

    # read current file if exists
    existing = {}
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    existing[k] = v

    openai_key = prompt_key("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", existing.get("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"))
    newsapi_key = prompt_key("NEWSAPI_KEY", existing.get("NEWSAPI_KEY"))

    existing["OPENAI_API_KEY"] = openai_key
    existing["NEWSAPI_KEY"] = newsapi_key

    with open(env_path, "w") as f:
        for k, v in existing.items():
            f.write(f"{k}={v}\n")

    print(f".env updated at {env_path}")


if __name__ == "__main__":
    main()
