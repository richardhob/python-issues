
import os
import shutil

import pytest

@pytest.fixture
def paths(tmp_path):
    normal = tmp_path / "normal.img"
    sparse = tmp_path / 'sparse.img'

    with open(normal, 'wb') as output:
        output.write(b'Test')

    with open(sparse, 'wb+') as output:
        os.truncate(sparse, 1024)

    return (tmp_path, normal, sparse)

def test_copy_normal(paths):
    (path, normal, _) = paths

    copy = path / 'test.img'
    shutil.copy(normal, copy)

    normal_stat = os.stat(normal)
    copy_stat = os.stat(copy)

    assert normal_stat.st_blocks == copy_stat.st_blocks

def test_copy_sparse(paths):
    (path, _, sparse) = paths

    copy = path / 'test.img'
    shutil.copy(sparse, copy)

    sparse_stat = os.stat(sparse)
    copy_stat = os.stat(copy)

    assert sparse_stat.st_blocks == copy_stat.st_blocks
