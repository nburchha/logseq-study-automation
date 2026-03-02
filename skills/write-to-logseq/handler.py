import os
import argparse
import json
import sys

def write_to_logseq(file_path, content, mode):
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)

        if mode == "create":
            if os.path.exists(file_path):
                return {"success": False, "error": f"File already exists: {file_path}"}
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
        
        elif mode == "overwrite":
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
        
        elif mode == "append":
            file_exists = os.path.exists(file_path)
            with open(file_path, "a", encoding="utf-8") as f:
                # Add newline if file exists and isn't empty
                if file_exists and os.path.getsize(file_path) > 0:
                    f.write("\n")
                f.write(content)
        
        return {"success": True, "path": os.path.abspath(file_path)}

    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    # This allows the skill to be called from the CLI
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", required=True)
    parser.add_argument("--content", required=True)
    parser.add_argument("--mode", choices=["create", "overwrite", "append"], required=True)
    args = parser.parse_args()

    result = write_to_logseq(args.file_path, args.content, args.mode)
    print(json.dumps(result))
