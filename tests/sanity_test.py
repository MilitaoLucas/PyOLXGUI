import pytest
import os

@pytest.fixture
def create_test_files(tmp_path):
    target_file = tmp_path / "target_file.txt"
    generated_correct = tmp_path / "generated_file_correct.txt"
    generated_incorrect = tmp_path / "generated_file_incorrect.txt"

    target_file.write_text("This is the target content.\nLine 2.")
    generated_correct.write_text("This is the target content.\nLine 2.")
    generated_incorrect.write_text("This is some different content.\nLine B.")

    return {
        "target": target_file,
        "correct": generated_correct,
        "incorrect": generated_incorrect,
    }

def _read_file_content(file_path):
    with open(file_path, 'r') as f:
        return f.read()

def test_correct_file_comparison_pytest(create_test_files):
    files = create_test_files
    target_content = _read_file_content(files["target"])
    generated_content = _read_file_content(files["correct"])
    assert target_content == generated_content, \
        "Correctly generated file content should match target."

def test_incorrect_file_comparison_pytest(create_test_files):
    files = create_test_files
    target_content = _read_file_content(files["target"])
    generated_content = _read_file_content(files["incorrect"])
    assert target_content != generated_content, \
        "Incorrectly generated file content should not match target."

def test_file_line_by_line_comparison(create_test_files):
    files = create_test_files
    with open(files["target"], 'r') as target_f, \
         open(files["correct"], 'r') as generated_f:
        # Compare line by line for more detailed error messages
        for i, (target_line, generated_line) in \
            enumerate(zip(target_f, generated_f)):
            assert target_line == generated_line, \
                f"Mismatch at line {i+1}: Expected '{target_line.strip()}', Got '{generated_line.strip()}'"
        
        # Ensure files have the same number of lines
        assert len(list(target_f)) == 0 and len(list(generated_f)) == 0, \
            "Files have different number of lines."