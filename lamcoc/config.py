import yaml
import os


def load_config(project_root):
    """Load include/exclude/libraries patterns from include.yaml in the user's project."""
    config_path = os.path.join(project_root, "include.yaml")

    if not os.path.exists(config_path):
        print(f"⚠️ Config file not found: {config_path}")
        return [], [], []

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
        return config.get("include", []), config.get("exclude", []), config.get("libraries", [])
