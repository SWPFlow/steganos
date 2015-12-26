import pytest
import unittest.mock
from ..src import steganos_decode
from ..src import steganos_encode

@pytest.mark.parametrize('length, expected', [
    (3, 'abc'),
    (5, 'abcab'),
    (2, 'ab')
])
def test_repeated_string(length, expected):
    assert expected == steganos_encode.repeat('abc', length)

@pytest.mark.parametrize('length, expected', [
    (3, ['a', 'b', 'c']),
    (5, ['a', 'b', 'c', 'a', 'b']),
    (2, ['a', 'b'])
])
def test_repeated_list(length, expected):
    assert expected == steganos_encode.repeat(['a', 'b', 'c'], length)

def test_filter_by_bits():
    # given
    bits = '101'
    xs = ['a', 'b', 'c']

    # when
    result = steganos_encode.filter_by_bits(xs, bits)

    # then
    assert result == ['a', 'c']

def test_make_change_for_single_change():
    # given
    text = 'This is his dog.'
    changes = [(9, 11, 'er')]

    # when
    result = steganos_encode.make_changes(text, changes)

    # then
    assert result == 'This is her dog.'

def test_make_changes_for_two_changes():
    # given
    text = 'This is his dog.'
    changes = [(9, 11, 'er'), (12, 15, 'cat')]

    # when
    result = steganos_encode.make_changes(text, changes)

    # then
    assert result == 'This is her cat.'

def test_make_changes_when_change_is_different_length():
    # given
    text = 'This is just a sample string.'
    changes = [(22, 28, 'text'), (0, 4, 'It')]

    # when
    result = steganos_encode.make_changes(text, changes)

    # then
    assert result == 'It is just a sample text.'

def test_execute_branchpoints_when_one_is_sandwiched():
    # given
    text = '"How is she?" he asked.'
    branchpoints = [
        [(0, 1, "'"), (12, 13, "'")],
        [(8, 9, '')]
    ]

    # when
    result = steganos_encode.execute_branchpoints(branchpoints, text)

    # then
    assert result == "'How is he?' he asked."


def test_encode():
    # given
    text = '"I am 9," he said.'
    bits = '01'

    # when
    result = steganos_encode.encode(bits, text)

    # then
    assert result == '"I am nine," he said\u200f\u200e.'

def test_encode_a_single_bit():
    # given
    text = '"I am 9," he said.'
    bits = '1'

    # when
    result = steganos_encode.encode(bits, text)

    # then
    assert result == "'I\u0083 am nine,' he said\u200f\u200e."

def test_encode_raises_when_given_too_many_bits_for_text():
    # given
    text = 'x'
    bits = '110'

    # then
    with pytest.raises(ValueError) as execinfo:
        steganos_encode.encode(bits, text)

    assert (str(steganos_encode.bit_capacity(text)) in str(execinfo.value)
            and str(len(bits)) in str(execinfo.value))

def test_bit_capacity():
    # given
    text = 'I am 9\t, but I say "I am 8."'

    # when
    result = steganos_encode.bit_capacity(text)

    # then
    assert result >= 3
