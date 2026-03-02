import os
import re
import json
import argparse

def manage_workflow_tags(file_path, add_tags=None, remove_tags=None):
    if add_tags is None: add_tags = []
    if remove_tags is None: remove_tags = []

    try:
        if not os.path.exists(file_path):
            return {"success": False, "error": f"File not found: {file_path}"}

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 1. Remove Tags
        for tag in remove_tags:
            # Match the tag with surrounding whitespace, but preserve a single space if it was between words
            # This regex handles tags at start/end or surrounded by spaces/newlines
            pattern = r'\s*' + re.escape(tag) + r'\b'
            content = re.sub(pattern, '', content).strip()

        # 2. Add Tags
        existing_tags = set(re.findall(r'#[\w-]+', content))
        tags_to_add = [t for t in add_tags if t not in existing_tags]

        if tags_to_add:
            # Check for Logseq 'tags::' property block (usually at the top)
            tags_property_match = re.search(r'^(tags::\s*)(.*)$', content, re.MULTILINE)
            
            if tags_property_match:
                # Append to existing tags:: line
                prefix = tags_property_match.group(1)
                current_tags = tags_property_match.group(2).strip()
                new_tags_str = ", ".join(tags_to_add)
                
                if current_tags:
                    updated_line = f"{prefix}{current_tags}, {new_tags_str}"
                else:
                    updated_line = f"{prefix}{new_tags_str}"
                
                content = content[:tags_property_match.start()] + updated_line + content[tags_property_match.end():]
            else:
                # Append to the end of the file
                tags_str = " ".join(tags_to_add)
                if not content.endswith("\n"):
                    content += "\n"
                content += f"\n{tags_str}"

        # 3. Write back
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return {
            "success": True,
            "updated_content": content
        }

    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", required=True)
    parser.add_argument("--add_tags", nargs='*', default=[])
    parser.add_argument("--remove_tags", nargs='*', default=[])
    args = parser.parse_args()

    result = manage_workflow_tags(args.file_path, args.add_tags, args.remove_tags)
    print(json.dumps(result))
