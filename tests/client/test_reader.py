import datetime as dt
import struct
import os
import pytest
import time

from wackywango.client import reader


user_id = 42
username = "Dan Gittik"
birthday = 699746400


@pytest.fixture
def reader_obj():
    return reader.Reader('tests/small_sample.mind.gz')


def test_user_attributes(reader_obj):
    # print(reader_obj.user)
    assert reader_obj.user.user_id == user_id
    assert reader_obj.user.username == username
    assert reader_obj.user.birthday == birthday


def test_only_2_snapshots(reader_obj):
    next(reader_obj)
    next(reader_obj)
    with pytest.raises(StopIteration):
        next(reader_obj)

def test_first_snapshot(reader_obj):
    first_snapshot = next(reader_obj)
    assert first_snapshot.snapshot.pose.translation.x == 0.4873843491077423
    assert first_snapshot.snapshot.pose.rotation.x == -0.10888676356214629
    assert first_snapshot.snapshot.feelings != None

def test_second_snapshot(reader_obj):
    next(reader_obj)
    second_snapshot = next(reader_obj)
    assert second_snapshot.snapshot.feelings.hunger == 0.0010000000474974513
    assert second_snapshot.snapshot.feelings.thirst == 0.003000000026077032
