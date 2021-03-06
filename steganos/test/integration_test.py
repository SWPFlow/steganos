import pytest
import os
import gzip
from ..src import steganos_decode
from ..src import steganos_encode

def test_when_global_change_out_of_encoded_text():
    # given
    text = 'I am 9, but I say "I am 8".'
    encoded_text = steganos_encode.encode('11', text)

    # when
    result = steganos_decode.decode_partial_text(encoded_text[0:9], text)

    # then
    assert '?1' in result

def test_local_changes_appear_after_global_changes_in_decoded_bits():
    # given
    text = 'I am 9\t, but I say "I am 8".'
    encoded_text = steganos_encode.encode('111', text)

    # when
    result = steganos_decode.decode_partial_text(encoded_text[0:15], text)

    # then
    assert '?11' in result

def test_global_change_late_in_encoded_text():
    # given
    text = 'I am 9\t, but I say "I am 8"'
    encoded_text = steganos_encode.encode('111', text)

    # when
    result = steganos_decode.decode_partial_text(encoded_text[33:], text)

    # then
    assert '11?' in result

def test_encode_and_decode():
    # given
    text = '"I am 9." he said.'
    bits = '01'
    encoded_text = steganos_encode.encode(bits, text)

    # when
    result = steganos_decode.decode_full_text(encoded_text, text)

    # then
    assert bits in result

def test_single_bit():
    # given
    text = '"I am 9." he said.'
    bits = '1'
    encoded_text = steganos_encode.encode(bits, text)

    # when
    result = steganos_decode.decode_full_text(encoded_text, text)

    # then
    assert '1111' in result

def test_bad_origin():
    # given
    original_text = 'This is a bad sentence with a 9.'
    encoded_text = 'This does not match with a 9.'

    # then
    with pytest.raises(ValueError):
        steganos_decode.decode_full_text(encoded_text, original_text)

def test_with_sample_fflabs_report():
    # given
    bits = '101010101011111111'
    filename = (os.path.dirname(os.path.abspath(__file__)) +
                '/sample_text.txt.gz')
    with gzip.open(filename) as book:
        text = book.read().decode('utf8')
    encoded_text = steganos_encode.encode(bits, text)

    # when
    result = steganos_decode.decode_full_text(encoded_text, text,
                                              message_bits=len(bits))

    # then
    assert bits == result

