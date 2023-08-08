
import os
import shutil

import pytest

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
