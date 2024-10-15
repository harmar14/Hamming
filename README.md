# Encoding and decoding by the Hamming algorithm with one error correction
**Encoder**
Input:
>python encoder.py 110
Output:
>Data after correction: {'data': '0110', 'check_bits_cnt': 3, 'info_bits_cnt': 4, 'hamming_length': 7}
>Performing encoding with Hamming (7, 4) algorithm...
>Encoded sequence: 1100110
**Decoder**
Input:
>python decoder.py 1100111
Output:
>Syndromes: ['1', '1', '1']
>Sequence 1100111 has error on index 6 (starting from 0). The corrected sequence is 1100110.
>Original sequence is 0110
