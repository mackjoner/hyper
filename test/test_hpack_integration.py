# -*- coding: utf-8 -*-
"""
This module defines substantial HPACK integration tests. These can take a very
long time to run, so they're outside the main test suite, but they need to be
run before every change to HPACK.
"""
from hyper.http20.hpack import Decoder, Encoder
from hyper.http20.huffman import HuffmanDecoder, HuffmanEncoder
from hyper.http20.huffman_constants import (
    REQUEST_CODES, REQUEST_CODES_LENGTH, REQUEST_CODES, REQUEST_CODES_LENGTH
)
from binascii import unhexlify
from pytest import skip

class TestHPACKDecoderIntegration(object):
    def test_can_decode_a_story(self, story):
        d = Decoder()

        # We support draft 7 of the HPACK spec.
        if story['draft'] != 7:
            skip("We support draft 7, not draft %d" % story['draft'])

        for case in story['cases']:
            try:
                d.header_table_size = case['header_table_size']
            except KeyError:
                pass
            decoded_headers = d.decode(unhexlify(case['wire']))
            decoded_headers = sorted(decoded_headers)

            # The correct headers are a list of dicts, which is annoying.
            correct_headers = [(item[0], item[1]) for header in case['headers'] for item in header.items()]
            correct_headers = sorted(correct_headers)
            assert correct_headers == decoded_headers

    def test_can_encode_a_story_no_huffman(self, raw_story):
        d = Decoder()
        e = Encoder()

        for case in raw_story['cases']:
            # The input headers are a list of dicts, which is annoying.
            input_headers = [(item[0], item[1]) for header in case['headers'] for item in header.items()]
            input_headers = sorted(input_headers)

            encoded = e.encode(input_headers, huffman=False)
            decoded_headers = d.decode(encoded)
            decoded_headers = sorted(decoded_headers)

            assert input_headers == decoded_headers

    def test_can_encode_a_story_with_huffman(self, raw_story):
        d = Decoder()
        e = Encoder()

        for case in raw_story['cases']:
            # The input headers are a list of dicts, which is annoying.
            input_headers = [(item[0], item[1]) for header in case['headers'] for item in header.items()]
            input_headers = sorted(input_headers)

            encoded = e.encode(input_headers, huffman=True)
            decoded_headers = d.decode(encoded)
            decoded_headers = sorted(decoded_headers)

            assert input_headers == decoded_headers
