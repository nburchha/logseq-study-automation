import os
import shutil
import sys

# Add the current directory to sys.path to import the handler
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from handler import manage_workflow_tags

def test_manage_workflow_tags():
    test_dir = os.path.join(os.path.dirname(__file__), "test_logseq")
    os.makedirs(test_dir, exist_ok=True)
    
    # 1. Test adding to tags:: property
    file_with_props = os.path.join(test_dir, "props.md")
    with open(file_with_props, "w") as f:
        f.write("tags:: #initial\ntitle:: Test Page\n\n- some content")
    
    print("Testing adding to tags:: property...")
    res = manage_workflow_tags(file_with_props, add_tags=["#anki-pending"])
    assert res["success"] == True
    assert "tags:: #initial, #anki-pending" in res["updated_content"]
    
    # 2. Test removing tags
    print("Testing removing tags...")
    res = manage_workflow_tags(file_with_props, remove_tags=["#initial"])
    assert res["success"] == True
    # The initial tag should be gone, but the property line and the other tag should remain
    assert "#initial" not in res["updated_content"]
    assert "#anki-pending" in res["updated_content"]

    # 3. Test appending to file without properties
    file_no_props = os.path.join(test_dir, "no_props.md")
    with open(file_no_props, "w") as f:
        f.write("- item 1\n- item 2")
    
    print("Testing appending to end of file...")
    res = manage_workflow_tags(file_no_props, add_tags=["#review-ready"])
    assert res["success"] == True
    assert res["updated_content"].strip().endswith("#review-ready")
    
    print("All manage-workflow-tags tests passed!")
    
    # Cleanup
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

if __name__ == "__main__":
    try:
        test_manage_workflow_tags()
    except AssertionError as e:
        print(f"Test failed!")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
