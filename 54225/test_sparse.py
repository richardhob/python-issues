
import os
import shutil

import pytest
import my_copy 

@pytest.fixture
def sparse_empty(tmp_path):
    path = tmp_path / "sparse_empty.img"
    with open(path, "ab") as out:
        out.truncate(1024)
    return path

@pytest.fixture
def sparse(tmp_path):
    path = tmp_path / "sparse.img"
    with open(path, "wb+") as out:
        fileno = out.fileno()
        out.truncate(1024)
        os.lseek(fileno, 0, os.SEEK_SET)
        out.write(b'\x01\x02\x03')

        os.lseek(fileno, -10, os.SEEK_END)
        out.write(b'\x04\x05\x06')

    return path

@pytest.fixture
def normal(tmp_path):
    path = tmp_path / "normal.img"
    with open(path, "ab") as out:
        out.write(b'\0' * 1024)
    return path

def test_sparse_empty(sparse_empty):
    assert os.stat(sparse_empty).st_size == 1024
    assert os.stat(sparse_empty).st_blocks * 512 == 0

def test_copy_sparse_empty(tmp_path, sparse_empty):
    copy = tmp_path / "copy.img"
    shutil.copyfile(sparse_empty, copy)
    assert os.stat(copy).st_size == 1024
    assert os.stat(copy).st_blocks * 512 == 0

def test_sparse(sparse):
    assert os.stat(sparse).st_size == 1024
    assert os.stat(sparse).st_blocks * 512 == 0

def test_copy_sparse_empty(tmp_path, sparse):
    copy = tmp_path / "copy.img"
    my_copy.copy_sparse(sparse, copy)
    # shutil.copyfile(sparse, copy)
    assert os.stat(copy).st_size == 1024
    assert os.stat(copy).st_blocks * 512 == 0

def test_normal(normal):
    assert os.stat(normal).st_size == 1024
    assert os.stat(normal).st_blocks * 512 == 8 * 512

def test_copy_normal(tmp_path, normal):
    copy = tmp_path / "normal_copy.img"
    shutil.copyfile(normal, copy)
    assert os.stat(copy).st_size == 1024
    assert os.stat(copy).st_blocks * 512 == 8 * 512
