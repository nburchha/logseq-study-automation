import os
import shutil
import sys

# Add the current directory to sys.path to import the handler
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from handler import write_to_logseq

def test_write_to_logseq():
    test_dir = os.path.join(os.path.dirname(__file__), "test_logseq")
    test_file = os.path.join(test_dir, "test_page.md")
    
    # Cleanup before starting
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    
    print("Testing 'create' mode...")
    # 1. Create a new file
    res = write_to_logseq(test_file, "First Line", "create")
    assert res["success"] == True
    assert os.path.exists(test_file)
    with open(test_file, "r") as f:
        assert f.read() == "First Line"
    
    # 2. Error on 'create' if exists
    res = write_to_logseq(test_file, "New Content", "create")
    assert res["success"] == False
    assert "already exists" in res["error"]
    
    print("Testing 'overwrite' mode...")
    # 3. Overwrite existing file
    res = write_to_logseq(test_file, "Overwritten", "overwrite")
    assert res["success"] == True
    with open(test_file, "r") as f:
        assert f.read() == "Overwritten"
    
    print("Testing 'append' mode...")
    # 4. Append content
    res = write_to_logseq(test_file, "Appended Line", "append")
    assert res["success"] == True
    with open(test_file, "r") as f:
        # Should have a newline separator
        content = f.read()
        assert content == "Overwritten\nAppended Line"
        
    print("All tests passed!")
    
    # Final cleanup
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

if __name__ == "__main__":
    try:
        test_write_to_logseq()
    except AssertionError as e:
        print(f"Test failed!")
        exit(1)
    except Exception as e:
        print(f"An error occurred during testing: {e}")
        exit(1)
