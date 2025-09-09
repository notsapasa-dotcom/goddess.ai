import os

APP_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app')

def print_file_contents(root):
    for dirpath, _, filenames in os.walk(root):
        for filename in sorted(filenames):
            if filename.startswith('.'):
                continue
            filepath = os.path.join(dirpath, filename)
            relpath = os.path.relpath(filepath, root)
            print(f"\n# {relpath}")
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    print(f.read())
            except Exception as e:
                print(f"[Error reading {relpath}: {e}]")

if __name__ == "__main__":
    if os.path.exists(APP_DIR):
        print_file_contents(APP_DIR)
    else:
        print(f"[app directory not found: {APP_DIR}]")
