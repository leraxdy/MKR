import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import pytest
import tempfile
from text_filter import (
    read_file,
    filter_lines,
    write_file,
    filter_text_file
)


# Fixtures
@pytest.fixture
def temp_input_file():
    """Create a temporary input file for testing."""
    with tempfile.NamedTemporaryFile(
        mode='w',
        encoding='utf-8',
        delete=False,
        suffix='.txt'
    ) as tmp:
        tmp.write("First line with Python\n")
        tmp.write("Second line without keyword\n")
        tmp.write("Third line with Python again\n")
        tmp.write("Fourth line\n")
        tmp.write("Python is great\n")
        tmp_path = tmp.name

    yield tmp_path

    # Cleanup
    if os.path.exists(tmp_path):
        os.unlink(tmp_path)


@pytest.fixture
def temp_output_file():
    """Create a temporary output file path."""
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix='.txt'
    ) as tmp:
        tmp_path = tmp.name

    yield tmp_path

    # Cleanup
    if os.path.exists(tmp_path):
        os.unlink(tmp_path)


@pytest.fixture
def sample_lines():
    """Provide sample lines for testing."""
    return [
        "Apple is red\n",
        "Banana is yellow\n",
        "Apple is sweet\n",
        "Orange is orange\n",
        "Apple pie is delicious\n"
    ]


# Tests for read_file function
def test_read_file_success(temp_input_file):
    """Test successful file reading."""
    lines = read_file(temp_input_file)
    assert len(lines) == 5
    assert "Python" in lines[0]


def test_read_file_not_found():
    """Test reading non-existent file."""
    with pytest.raises(FileNotFoundError, match="File nonexistent.txt not found"):
        read_file("nonexistent.txt")


# Tests for filter_lines with parametrization
@pytest.mark.parametrize("lines,keyword,expected_count", [
    (["line1\n", "line2\n", "line3\n"], "line", 3),
    (["Python\n", "Java\n", "Python\n"], "Python", 2),
    (["No match here\n", "Another line\n"], "keyword", 0),
    ([], "anything", 0),
    (["Case sensitive\n"], "case", 0),
])
def test_filter_lines_parametrized(lines, keyword, expected_count):
    """Test filter_lines with various inputs using parametrization."""
    result = filter_lines(lines, keyword)
    assert len(result) == expected_count


def test_filter_lines_empty_keyword():
    """Test filtering with empty keyword."""
    lines = ["line1\n", "line2\n"]
    result = filter_lines(lines, "")
    assert result == []


def test_filter_lines_with_keyword_match(sample_lines):
    """Test filtering lines that contain specific keyword."""
    result = filter_lines(sample_lines, "Apple")
    assert len(result) == 3
    assert all("Apple" in line for line in result)


# Tests for write_file function
def test_write_file_success(temp_output_file):
    """Test successful file writing."""
    lines = ["Hello\n", "World\n"]
    write_file(temp_output_file, lines)

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        content = f.readlines()
    assert content == lines


def test_write_file_invalid_path():
    """Test writing to invalid path."""
    with pytest.raises(IOError):
        write_file("/invalid/path/file.txt", ["line\n"])


# Tests for filter_text_file function
def test_filter_text_file_integration(temp_input_file, temp_output_file):
    """Test complete filter functionality."""
    keyword = "Python"
    count = filter_text_file(temp_input_file, temp_output_file, keyword)

    assert count == 3

    with open(temp_output_file, 'r', encoding='utf-8') as f:
        filtered_content = f.read()

    assert "Python" in filtered_content
    assert "without keyword" not in filtered_content


def test_filter_text_file_empty_result(temp_input_file, temp_output_file):
    """Test filtering with keyword that produces empty result."""
    count = filter_text_file(temp_input_file, temp_output_file, "Nonexistent")
    assert count == 0


def test_filter_text_file_input_not_found(temp_output_file):
    """Test filtering with non-existent input file."""
    with pytest.raises(FileNotFoundError):
        filter_text_file("nonexistent.txt", temp_output_file, "test")