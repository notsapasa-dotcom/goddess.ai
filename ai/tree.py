import os

def print_tree(root, prefix=""):
    entries = [e for e in os.listdir(root) if not e.startswith('.') and e not in {'.git', '__pycache__', 'node_modules', '.venv', 'venv'}]
    entries.sort()
    for i, entry in enumerate(entries):
        path = os.path.join(root, entry)
        connector = "└── " if i == len(entries) - 1 else "├── "
        print(prefix + connector + entry)
        if os.path.isdir(path):
            extension = "    " if i == len(entries) - 1 else "│   "
            print_tree(path, prefix + extension)

if __name__ == "__main__":
    print(os.path.basename(os.getcwd()))
    print_tree(os.getcwd())
