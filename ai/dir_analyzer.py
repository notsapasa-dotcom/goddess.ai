import os
import sys
import json
import hashlib
from pathlib import Path
from typing import List, Optional, Dict
from datetime import datetime

class AIDirectoryAnalyzer:
    def __init__(self, root_dir: str, ignore_dirs: Optional[List[str]] = None):
        """Initialize the analyzer with root directory and ignore patterns."""
        self.root_dir = root_dir
        self.ignore_dirs = ignore_dirs or ['.git', '__pycache__', 'node_modules', '.venv', 'venv']
        self.structure = self._init_structure()

    def _init_structure(self) -> Dict:
        """Initialize the data structure with metadata."""
        return {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "root_path": str(Path(self.root_dir).resolve()),
                "version": "1.0",
                "analyzer_id": hashlib.md5(str(datetime.now().timestamp()).encode()).hexdigest()
            },
            "structure": {},
            "stats": {
                "total_files": 0,
                "total_dirs": 0,
                "file_types": {},
                "max_depth": 0,
                "total_size": 0,
                "newest_file": None,
                "oldest_file": None
            },
            "errors": []
        }

    def _should_ignore(self, name: str) -> bool:
        """Determine if a file or directory should be ignored."""
        return name.startswith('.') or name in self.ignore_dirs

    def _compute_file_hash(self, filepath: str, block_size: int = 65536) -> str:
        """Compute MD5 hash of file for change detection."""
        hasher = hashlib.md5()
        try:
            with open(filepath, 'rb') as f:
                for block in iter(lambda: f.read(block_size), b''):
                    hasher.update(block)
            return hasher.hexdigest()
        except Exception as e:
            self.structure["errors"].append({
                "type": "hash_computation_error",
                "path": filepath,
                "error": str(e)
            })
            return None

    def _update_stats(self, file_info: Dict) -> None:
        """Update statistical information."""
        stats = self.structure["stats"]
        
        # Update file type stats
        ext = file_info.get("extension", "no_extension")
        stats["file_types"][ext] = stats["file_types"].get(ext, 0) + 1
        
        # Update total size
        stats["total_size"] += file_info.get("size", 0)
        
        # Update timestamp stats
        mod_time = datetime.fromisoformat(file_info["last_modified"])
        if not stats["newest_file"] or mod_time > datetime.fromisoformat(stats["newest_file"]["timestamp"]):
            stats["newest_file"] = {
                "path": file_info["path"],
                "timestamp": file_info["last_modified"]
            }
        if not stats["oldest_file"] or mod_time < datetime.fromisoformat(stats["oldest_file"]["timestamp"]):
            stats["oldest_file"] = {
                "path": file_info["path"],
                "timestamp": file_info["last_modified"]
            }

    def analyze(self, directory: str = None, depth: int = 0) -> Dict:
        """Generate machine-readable directory structure with detailed metadata."""
        if directory is None:
            directory = self.root_dir

        current_dir = {}
        try:
            entries = os.listdir(directory)
        except PermissionError:
            self.structure["errors"].append({
                "type": "permission_denied",
                "path": directory
            })
            return {"error": "permission_denied"}

        # Update max depth
        self.structure["stats"]["max_depth"] = max(self.structure["stats"]["max_depth"], depth)
        
        # Sort entries for consistent output
        entries.sort()

        for entry in entries:
            if self._should_ignore(entry):
                continue

            path = os.path.join(directory, entry)
            rel_path = str(Path(path).relative_to(self.root_dir))

            try:
                if os.path.isdir(path):
                    self.structure["stats"]["total_dirs"] += 1
                    current_dir[entry] = {
                        "type": "directory",
                        "path": rel_path,
                        "contents": self.analyze(path, depth + 1),
                        "last_modified": datetime.fromtimestamp(os.path.getmtime(path)).isoformat()
                    }
                else:
                    self.structure["stats"]["total_files"] += 1
                    file_info = {
                        "type": "file",
                        "path": rel_path,
                        "size": os.path.getsize(path),
                        "extension": os.path.splitext(entry)[1].lower() or None,
                        "last_modified": datetime.fromtimestamp(os.path.getmtime(path)).isoformat(),
                        "hash": self._compute_file_hash(path)
                    }
                    current_dir[entry] = file_info
                    self._update_stats(file_info)

            except Exception as e:
                self.structure["errors"].append({
                    "type": "processing_error",
                    "path": rel_path,
                    "error": str(e)
                })

        return current_dir

    def generate_structure(self) -> None:
        """Generate the complete structure."""
        self.structure["structure"] = self.analyze()

    def save_to_file(self, output_file: str = "ai_directory_structure.json") -> None:
        """Save the structure in JSON format."""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.structure, f, indent=2)
        except Exception as e:
            self.structure["errors"].append({
                "type": "save_error",
                "path": output_file,
                "error": str(e)
            })

    def get_structure(self) -> Dict:
        """Return the structure as a dictionary."""
        return self.structure

def main():
    """Main execution function."""
    try:
        # Get the project root directory (one level up from this script)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(script_dir)
        
        # Create and generate the analysis
        analyzer = AIDirectoryAnalyzer(root_dir)
        analyzer.generate_structure()
        
        # Save to file in the ai directory
        output_file = os.path.join(script_dir, "ai_directory_structure.json")
        analyzer.save_to_file(output_file)
        
        # Return success status for machine processing
        sys.exit(0)
    except Exception as e:
        # Return error status for machine processing
        sys.stderr.write(f"Error: {str(e)}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
