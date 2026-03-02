import os
import re
import json
import argparse

def manage_workflow_tags(file_path, action, tag=None, old_tag=None, new_tag=None, block_id=None, block_content=None):
    try:
        if not os.path.exists(file_path):
            return {"success": False, "error": f"File not found: {file_path}"}

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Targeting: Block or File
        if block_id or block_content:
            lines = content.splitlines(keepends=True)
            start_idx = None
            for i, line in enumerate(lines):
                if block_id and f"id:: {block_id}" in line:
                    start_idx = i
                    while start_idx >= 0 and not lines[start_idx].strip().startswith("- "):
                        start_idx -= 1
                    break
                elif block_content and line.strip().startswith("- ") and block_content in line:
                    start_idx = i
                    break
            
            if start_idx is not None:
                first_line = lines[start_idx]
                indent = len(first_line) - len(first_line.lstrip())
                end_idx = start_idx + 1
                while end_idx < len(lines):
                    curr_line = lines[end_idx]
                    if curr_line.strip().startswith("- "):
                        if (len(curr_line) - len(curr_line.lstrip())) <= indent:
                            break
                    end_idx += 1
                
                block_lines = lines[start_idx:end_idx]
                updated_block = apply_action("".join(block_lines), action, tag, old_tag, new_tag, is_block=True)
                lines[start_idx:end_idx] = [updated_block]
                content = "".join(lines)
            else:
                return {"success": False, "error": f"Block not found (id={block_id}, content={block_content})"}
        else:
            # File-level logic
            content = apply_action(content, action, tag, old_tag, new_tag, is_block=False)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return {"success": True, "updated_content": content}

    except Exception as e:
        return {"success": False, "error": str(e)}

def apply_action(text, action, tag, old_tag, new_tag, is_block=False):
    if action == "replace":
        if not old_tag or not new_tag:
            raise ValueError("replace requires old_tag and new_tag")
        pattern = re.escape(old_tag) + r'\b'
        return re.sub(pattern, new_tag, text)
    
    elif action == "remove":
        if not tag:
            raise ValueError("remove requires tag")
        pattern = r'\s*' + re.escape(tag) + r'\b'
        return re.sub(pattern, '', text).strip() if not is_block else re.sub(pattern, '', text)

    elif action == "add":
        if not tag:
            raise ValueError("add requires tag")
        if tag in text: # Simple check to avoid duplicates
            return text
        
        if is_block:
            # Add to the first line of the block
            lines = text.splitlines(keepends=True)
            first_line = lines[0].rstrip()
            lines[0] = f"{first_line} {tag}\n"
            return "".join(lines)
        else:
            # Add to tags:: property or append to end
            tags_prop_match = re.search(r'^(tags::\s*)(.*)$', text, re.MULTILINE)
            if tags_prop_match:
                prefix, current = tags_prop_match.groups()
                sep = ", " if current.strip() else ""
                updated = f"{prefix}{current.strip()}{sep}{tag}"
                return text[:tags_prop_match.start()] + updated + text[tags_prop_match.end():]
            else:
                return text.rstrip() + f"\n\n{tag}\n"
    
    return text

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", required=True)
    parser.add_argument("--action", choices=["add", "remove", "replace"], required=True)
    parser.add_argument("--tag")
    parser.add_argument("--old_tag")
    parser.add_argument("--new_tag")
    parser.add_argument("--block_id")
    parser.add_argument("--block_content")
    args = parser.parse_args()

    result = manage_workflow_tags(
        args.file_path, args.action, args.tag, args.old_tag, args.new_tag, args.block_id, args.block_content
    )
    print(json.dumps(result))
