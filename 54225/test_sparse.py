
import os

import pytest

@pytest.fixture
def sparse(tmp_path):
    path = tmp_path / "sparse.img"
    with open(path, "ab") as out:
        out.truncate(1024)
    return path

def test_sparse(sparse):
    assert os.stat(sparse).st_size == 1024
    assert os.stat(sparse).st_blocks*512 == 0
