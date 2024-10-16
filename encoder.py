from sys import argv

def check_data(data):
    check_set = set(data)
    if (check_set == {'0', '1'} or check_set == {'0'} or check_set == {'1'}):
        return True
    else:
        return False

def correct_data_to_encode(data):
    # Number of information bits before correction.
    i = len(data)
    # Number of check bits.
    r = 0
    while not ((2 ** r) >= r + i + 1):
        r += 1
    # Number of information bits after correction.
    i_corrected = 2 ** r - r - 1
    # Data correction.
    if (i != i_corrected):
        return {"data":data.rjust(i_corrected, '0'), "check_bits_cnt":r, "info_bits_cnt":i_corrected, "hamming_length":(i_corrected + r)}
    else:
        return {"data":data, "check_bits_cnt":r, "info_bits_cnt":i_corrected, "hamming_length":(i_corrected + r)}

def calculate_check_bit(bits_str, idx, distance):
    sequence = ''
    while (idx < len(bits_str)):
        sequence += bits_str[idx:(idx + distance)]
        idx = idx + distance * 2
    # Creating int list out of sequence.
    sequence = list(map(int, list(sequence)))
    # Calculating the check bit.
    check_bit = None
    for i in range(1, len(sequence)):
        if (check_bit is None):
            check_bit = sequence[i]
        else:
            check_bit = check_bit ^ sequence[i]
    return check_bit

def add_check_bits(info):
    bits = []
    data = info["data"]
    power = 0
    data_idx = 0
    # Adding zeros on positions of check bits.
    for bit_idx in range(info["hamming_length"]):
        if (bit_idx + 1 == 2 ** power):
            bits.append('0')
            power += 1
        else:
            bits.append(data[data_idx])
            data_idx += 1
    # Converting array of bits into string.
    bits_str = ''.join(bits)
    # Recalculating check bits.
    for check_bit_num in range (info["check_bits_cnt"]):
        power = 2 ** check_bit_num
        bits[power - 1] = str(calculate_check_bit(bits_str, (power - 1), power))
    return bits

def hamming_encode(data):
    info = correct_data_to_encode(data)
    print("Data after correction:", info)
    print(f"Performing encoding with Hamming ({info['hamming_length']}, {info['info_bits_cnt']}) algorithm...")
    bits = add_check_bits(info)
    print("Encoded sequence:", ''.join(bits))

if __name__ == '__main__':
    _, data_to_encode = argv
    if (check_data(data_to_encode)):
        hamming_encode(data_to_encode)
    else:
        print("Error: Binary sequence should be provided.")
