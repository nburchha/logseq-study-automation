import os
import shutil
import json
from handler import manage_workflow_tags

def test_single_action_workflow():
    test_dir = os.path.join(os.path.dirname(__file__), "test_logseq_new")
    os.makedirs(test_dir, exist_ok=True)
    
    # 1. Test File-level Add
    file_path = os.path.join(test_dir, "file_add.md")
    with open(file_path, "w") as f:
        f.write("tags:: #existing")
    
    print("Testing file-level add...")
    res = manage_workflow_tags(file_path, action="add", tag="#new")
    assert res["success"] == True
    assert "#new" in res["updated_content"]
    assert "tags:: #existing, #new" in res["updated_content"]

    # 2. Test Block-level Replace
    block_file = os.path.join(test_dir, "block_replace.md")
    with open(block_file, "w") as f:
        f.write("- block 1 #old\n  id:: 123\n- block 2 #old")
    
    print("Testing block-level replace...")
    res = manage_workflow_tags(block_file, action="replace", old_tag="#old", new_tag="#new", block_id="123")
    assert res["success"] == True
    assert "- block 1 #new" in res["updated_content"]
    assert "- block 2 #old" in res["updated_content"]

    # 3. Test Block-level Remove
    res = manage_workflow_tags(block_file, action="remove", tag="#new", block_id="123")
    assert res["success"] == True
    assert "- block 1" in res["updated_content"]
    assert "#new" not in res["updated_content"].splitlines()[0]

    # Cleanup
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    print("All redesigned tests passed!")

if __name__ == "__main__":
    try:
        test_single_action_workflow()
    except AssertionError as e:
        print(f"Test failed!")
        exit(1)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
