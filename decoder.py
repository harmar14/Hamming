from sys import argv
import math

def check_data(data):
    if ((set(data) == {'0', '1'} or set(data) == {'0'} or set(data) == {'1'}) and math.log2(len(data) + 1).is_integer()):
        return True
    else:
        return False

def calc_bits_cnt(data):
    data_length = len(data)
    check_bits_cnt = math.ceil(math.log2(data_length + 1))
    info_bits_cnt = data_length - check_bits_cnt
    return {"data":data, "check_bits_cnt":check_bits_cnt, "info_bits_cnt":info_bits_cnt, "hamming_length":data_length}

def calculate_syndrome(bits_str, idx, distance):
    sequence = ''
    while (idx < len(bits_str)):
        sequence += bits_str[idx:(idx + distance)]
        idx = idx + distance * 2
    # Creating int list out of sequence.
    sequence = list(map(int, list(sequence)))
    # Calculating the check bit.
    syndrome = None
    for i in range(len(sequence)):
        if (syndrome is None):
            syndrome = sequence[i]
        else:
            syndrome = syndrome ^ sequence[i]
    return syndrome

def calculate_all_syndromes(info):
    syndromes = []
    power = 0
    for check_bit_num in range (info["check_bits_cnt"]):
        power = 2 ** check_bit_num
        syndromes.append(str(calculate_syndrome(info["data"], (power - 1), power)))
    print("Syndromes:", syndromes)
    return syndromes

def find_error(info):
    # Searching for error using syndromes.
    syndromes = calculate_all_syndromes(info)
    reversed_syndromes = ''.join(syndromes)[::-1]
    error_idx = int(reversed_syndromes, 2) - 1
    return error_idx

def process_error(sequence, error_idx):
    if (error_idx == 0):
        print("Sequence is correct.")
        return sequence
    else:
        correction = '1' if (sequence[error_idx] == '0') else '0'
        sequence_corrected = sequence[:error_idx] + correction + sequence[(error_idx + 1):]
        print(f"Sequence {sequence} has error on index {error_idx} (starting from 0). The corrected sequence is {sequence_corrected}.")
        return sequence_corrected

def extract_information_bits(data, check_bits_cnt, length):
    power = 0
    information = ''
    # Getting rid of check bits.
    for i in range(length):
        if (i + 1 == 2 ** power):
            power += 1
        else:
            information += data[i]
    return information

def hamming_decode(data):
    info = calc_bits_cnt(data)
    data_corrected = process_error(info["data"], find_error(info))
    information_bits = extract_information_bits(data_corrected, info["check_bits_cnt"], info["hamming_length"])
    print("Original sequence is", information_bits)

if __name__ == '__main__':
    _, encodedData = argv
    if (check_data(encodedData)):
        hamming_decode(encodedData)
    else:
        print("Error: Invalid sequence provided.")