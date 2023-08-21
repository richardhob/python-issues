
import os
import shutil
from pathlib import Path
import unittest.mock

import stat
import errno

import pytest

def merge_request_onerror(func, path, exc):
    excvalue = exc[1]
    if excvalue.errno == errno.EACCES:
        if func in (os.rmdir, os.remove):
            parent_path = Path(path).parent
            os.chmod(parent_path, stat.S_IRWXU) # 0700
            func(path)
        elif func is os.listdir:
            os.chmod(path, stat.S_IRWXU) # 0700
            shutil.rmtree(path, ignore_errors=False, onerror=merge_request_onerror)
    else:
        raise ValueError("Could not find a way to fix")

LEVEL_1 = ['a', 'b', 'c']
LEVEL_2 = ['a1', 'b1', 'c1']
LEVEL_3 = ['a11', 'b11', 'c11']

@pytest.fixture
def tree(request, tmp_path):
    def _md(path):
        path.mkdir()

    for level_1 in LEVEL_1:
        _md(tmp_path / level_1)
        for level_2 in LEVEL_2:
            _md(tmp_path / level_1 / level_2)
            for level_3 in LEVEL_3:
                _md(tmp_path / level_1 / level_2 / level_3)

    path = tmp_path / 'a'/ 'a1'
    path.chmod(0o555)

    def _undo_chmod():
        if path.exists():
            path.chmod(0o750)

    request.addfinalizer(_undo_chmod)

    return tmp_path

def test_rmtree(tree):
    with pytest.raises(PermissionError):
        shutil.rmtree(tree)

def test_rmtree_no_fix(tree):
    def no_fix(function, path, exc_info):
        raise ValueError("Could not fix")

    with pytest.raises(ValueError):
        shutil.rmtree(tree, onerror=no_fix)

def test_rmtree_no_fix_no_error(tree):
    def no_fix(function, path, exc_info):
        pass

    shutil.rmtree(tree, onerror=no_fix)

def test_rmtree_fix_merge_request(tree):
    shutil.rmtree(tree, onerror=merge_request_onerror)

def test_rmtree_error_listdir():
    my_onerror = unittest.mock.MagicMock()
    errors = shutil.rmtree('DOES NOT EXIST DIR 123', onerror=my_onerror)
    my_onerror.assert_called_once()
    assert errors == []

def test_rmtree_error_ignore(tree):
    errors = shutil.rmtree(tree, ignore_errors=True)
    assert len(errors) == 6
