import subprocess
import json
import os

def test_read():
    print("Testing read action...")
    cmd = ["python3", "skills/read-and-search-logseq/handler.py", "--action", "read", "--file_path", "pages/test.md"]
    res = json.loads(subprocess.check_output(cmd, text=True))
    assert res["success"] == True
    assert "status::" in res["results"][0]["content"]
    print("Read test passed.")

def test_search_file():
    print("Testing search action (scope: file)...")
    cmd = ["python3", "skills/read-and-search-logseq/handler.py", "--action", "search", "--query", "anki-processed", "--search_scope", "file"]
    res = json.loads(subprocess.check_output(cmd, text=True))
    assert res["success"] == True
    assert any("pages/test.md" in r["file_path"] for r in res["results"])
    print("Search (file) test passed.")

def test_search_block():
    print("Testing search action (scope: block)...")
    # Using a string known to be in a specific block in pages/test.md
    cmd = ["python3", "skills/read-and-search-logseq/handler.py", "--action", "search", "--query", "hello world", "--search_scope", "block"]
    res = json.loads(subprocess.check_output(cmd, text=True))
    assert res["success"] == True
    # Should find individual blocks containing "hello world"
    assert any("hello world" in r["content"] for r in res["results"])
    print("Search (block) test passed.")

if __name__ == "__main__":
    try:
        test_read()
        test_search_file()
        test_search_block()
        print("All tests passed!")
    except Exception as e:
        print(f"Tests failed: {e}")
        exit(1)
