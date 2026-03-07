import os
import argparse
import json
import sys
import subprocess
import re


def git_commit(file_path, message):
    try:
        repo_dir = os.path.dirname(os.path.abspath(file_path))
        filename = os.path.basename(file_path)
        # Use -f to override local ignore rules if any for testing
        subprocess.run(
            ["git", "add", "-f", filename],
            cwd=repo_dir,
            check=True,
            capture_output=True,
        )
        res = subprocess.run(
            ["git", "commit", "-m", message],
            cwd=repo_dir,
            capture_output=True,
            text=True,
        )
        if (
            res.returncode != 0
            and "nothing to commit" not in res.stdout
            and "working tree clean" not in res.stdout
        ):
            pass
    except subprocess.CalledProcessError as e:
        pass  # Ignore if no changes or not a git repo


def write_to_logseq(file_path, content, mode, parent_block_query=None):
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)

        # Pre-commit (safety wrapper)
        git_commit(
            file_path, f"Pre-commit before AI write to {os.path.basename(file_path)}"
        )

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

        elif mode == "append_child_to_block":
            if not parent_block_query:
                return {
                    "success": False,
                    "error": "parent_block_query required for append_child_to_block",
                }
            if not os.path.exists(file_path):
                return {"success": False, "error": f"File not found: {file_path}"}

            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            target_idx = -1
            indent_str = ""
            for i, line in enumerate(lines):
                if parent_block_query in line:
                    target_idx = i
                    match = re.match(r"^(\s*)", line)
                    if match:
                        indent_str = match.group(1)
                    break

            if target_idx == -1:
                return {
                    "success": False,
                    "error": f"Block matching '{parent_block_query}' not found.",
                }

            # Find the end of this block's children to append at the bottom of the block
            insert_idx = target_idx + 1
            base_indent_len = len(indent_str)

            while insert_idx < len(lines):
                next_line = lines[insert_idx]
                if not next_line.strip():
                    insert_idx += 1
                    continue
                next_match = re.match(r"^(\s*)-\s+", next_line)
                if next_match:
                    next_indent = len(next_match.group(1))
                    if next_indent <= base_indent_len:
                        break  # Found next sibling or parent
                insert_idx += 1

            # Assuming 2 spaces for child indentation
            child_indent = indent_str + "  "

            # Format the incoming content to match the child indentation
            formatted_content = ""
            for line in content.splitlines():
                if line.strip().startswith("- "):
                    formatted_content += child_indent + line + "\n"
                else:
                    formatted_content += child_indent + "- " + line + "\n"

            lines.insert(insert_idx, formatted_content)

            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(lines)

        # Post-commit (safety wrapper)
        git_commit(file_path, f"AI {mode} to {os.path.basename(file_path)}")

        return {"success": True, "path": os.path.abspath(file_path)}

    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", required=True)
    parser.add_argument("--content", required=True)
    parser.add_argument(
        "--mode",
        choices=["create", "overwrite", "append", "append_child_to_block"],
        required=True,
    )
    parser.add_argument(
        "--parent_block_query",
        help="Text to identify the parent block when using append_child_to_block",
    )
    args = parser.parse_args()

    result = write_to_logseq(
        args.file_path, args.content, args.mode, args.parent_block_query
    )
    print(json.dumps(result))
