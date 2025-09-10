import os
import sys
import json
from pathlib import Path
from typing import List, Optional, Dict
from datetime import datetime

class AIDirectoryAnalyzer:
    def __init__(self, root_dir: str, ignore_dirs: Optional[List[str]] = None):
        self.root_dir = root_dir
        self.ignore_dirs = ignore_dirs or ['.git', '__pycache__', 'node_modules', '.venv', 'venv']
        self.structure = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "root_path": str(Path(root_dir).resolve()),
                "version": "1.0"
            },
            "structure": {},
            "stats": {
                "total_files": 0,
                "total_dirs": 0,
                "file_types": {},
                "max_depth": 0
            }
        }

    def _should_ignore(self, name: str) -> bool:
        return name.startswith('.') or name in self.ignore_dirs

    def _analyze_file_type(self, filename: str) -> None:
        """Track file extension statistics."""
        ext = os.path.splitext(filename)[1].lower() or 'no_extension'
        self.structure["stats"]["file_types"][ext] = self.structure["stats"]["file_types"].get(ext, 0) + 1

    def analyze(self, directory: str = None, depth: int = 0) -> Dict:
        """Generate machine-readable directory structure."""
        if directory is None:
            directory = self.root_dir

        current_dir = {}
        try:
            entries = os.listdir(directory)
        except PermissionError:
            return {"error": "permission_denied"}

        # Update max depth
        self.structure["stats"]["max_depth"] = max(self.structure["stats"]["max_depth"], depth)

        # Sort entries for consistent output
        entries.sort()

        for entry in entries:
            if self._should_ignore(entry):
                continue

            path = os.path.join(directory, entry)
            if os.path.isdir(path):
                self.structure["stats"]["total_dirs"] += 1
                current_dir[entry] = {
                    "type": "directory",
                    "path": str(Path(path).relative_to(self.root_dir)),
                    "contents": self.analyze(path, depth + 1)
                }
            else:
                self.structure["stats"]["total_files"] += 1
                self._analyze_file_type(entry)
                current_dir[entry] = {
                    "type": "file",
                    "path": str(Path(path).relative_to(self.root_dir)),
                    "size": os.path.getsize(path),
                    "extension": os.path.splitext(entry)[1].lower() or None,
                    "last_modified": datetime.fromtimestamp(os.path.getmtime(path)).isoformat()
                }

        return current_dir

    def generate_structure(self) -> None:
        """Generate the complete structure."""
        self.structure["structure"] = self.analyze()

    def save_to_file(self, output_file: str = "ai_directory_structure.json") -> None:
        """Save the structure in JSON format."""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.structure, f, indent=2)

    def get_structure(self) -> Dict:
        """Return the structure as a dictionary."""
        return self.structure

def main():
    # Get the project root directory (one level up from this script)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    
    # Create and generate the analysis
    analyzer = AIDirectoryAnalyzer(root_dir)
    analyzer.generate_structure()
    
    # Save to file in the ai directory
    output_file = os.path.join(script_dir, "ai_directory_structure.json")

if __name__ == "__main__":
    main()
