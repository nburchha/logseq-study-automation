import os
import sys
import json
import argparse
import subprocess
import re

def get_block_from_line(lines, line_idx):
    """Isolate a Logseq block (bullet + children)."""
    line = lines[line_idx]
    # Identify initial indentation
    indent_match = re.match(r'^(\s*-\s+)', line)
    if not indent_match:
        # Not a bullet line, but could be inside a block. Search up for bullet.
        curr = line_idx
        while curr >= 0:
            indent_match = re.match(r'^(\s*-\s+)', lines[curr])
            if indent_match:
                line_idx = curr
                break
            curr -= 1
        if not indent_match:
            return line, None # Fallback

    indent_str = indent_match.group(1)
    base_indent = len(indent_str.replace('-', ' '))
    
    block_lines = [lines[line_idx]]
    block_id = None
    
    # Capture subsequent lines belonging to the same block
    for i in range(line_idx + 1, len(lines)):
        curr_line = lines[i]
        if not curr_line.strip():
            block_lines.append(curr_line)
            continue
            
        curr_indent_match = re.match(r'^(\s*)', curr_line)
        curr_indent = len(curr_indent_match.group(1))
        
        # Logseq block ends if a line has less or equal indentation and starts with a bullet
        is_bullet = re.match(r'^\s*-\s+', curr_line)
        if is_bullet and curr_indent <= base_indent - 2: # Very rough heuristic
             # Actually, simpler: if it's a bullet and indent <= base_indent - (bullet size)
             pass

        # Robust way: If it's a bullet and indent <= base_indent (excluding bullet chars)
        if is_bullet:
            curr_base_indent = len(re.match(r'^(\s*-\s+)', curr_line).group(1).replace('-', ' '))
            if curr_base_indent <= base_indent:
                break
        
        # Check for block ID
        id_match = re.search(r'id:: ([a-f0-9\-]{36})', curr_line)
        if id_match:
            block_id = id_match.group(1)
            
        block_lines.append(curr_line)

    return "".join(block_lines), block_id

def search_logseq(query, search_scope="file"):
    results = []
    # Using grep for speed
    try:
        # Search in pages/ and journals/
        cmd = ["grep", "-rl", query, "pages/", "journals/"]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
        files = output.strip().split('\n')
    except subprocess.CalledProcessError:
        files = []

    for file_path in files:
        if not os.path.exists(file_path):
            continue
            
        with open(file_path, 'r') as f:
            content = f.read()
            
        if search_scope == "file":
            results.append({"file_path": file_path, "content": content})
        else:
            # Block-level search
            lines = content.splitlines(keepends=True)
            seen_blocks = set()
            for idx, line in enumerate(lines):
                if query in line:
                    block_content, block_id = get_block_from_line(lines, idx)
                    if block_content not in seen_blocks:
                        results.append({
                            "file_path": file_path, 
                            "content": block_content.strip(), 
                            "block_id": block_id
                        })
                        seen_blocks.add(block_content)
    
    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", choices=["read", "search"], required=True)
    parser.add_argument("--file_path")
    parser.add_argument("--query")
    parser.add_argument("--search_scope", choices=["file", "block"], default="file")
    
    args = parser.parse_args()
    
    try:
        if args.action == "read":
            if not args.file_path:
                print(json.dumps({"success": False, "error": "file_path required for read"}))
                return
            with open(args.file_path, 'r') as f:
                content = f.read()
            print(json.dumps({"success": True, "results": [{"file_path": args.file_path, "content": content}]}))
            
        elif args.action == "search":
            if not args.query:
                print(json.dumps({"success": False, "error": "query required for search"}))
                return
            results = search_logseq(args.query, args.search_scope)
            print(json.dumps({"success": True, "results": results}))
            
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))

if __name__ == "__main__":
    main()
