import os
import io
import math


def get_hexdump_lines(bs: bytes):
    number_of_bytes = len(bs)
    number_of_lines = math.ceil(number_of_bytes / 8)
    hexdump_lines = []
    for i in range(number_of_lines):
        line_bs = bs[i*8:(i+1)*8]
        line_content = ' '.join(['{:02x}'.format(b) for b in line_bs])
        hexdump_lines.append(line_content)

    return hexdump_lines


def print_hexdump_side_by_side(bs1: bytes, bs2: bytes):
    hexdump_lines1 = get_hexdump_lines(bs1)
    number_of_lines1 = len(hexdump_lines1)
    hexdump_lines2 = get_hexdump_lines(bs2)
    number_of_lines2 = len(hexdump_lines2)
    max_number_of_lines = max(number_of_lines1, number_of_lines2)
    for i in range(max_number_of_lines):
        if i < number_of_lines1:
            print(f'{hexdump_lines1[i]:24}', end='\t')
        else:
            print(' '*24, end='\t')

        if i < number_of_lines2:
            print(hexdump_lines2[i])
        else:
            print()


def get_all_child_files(filepath: str, outlog: list):
    if os.path.isfile(filepath):
        outlog.append(filepath)
    elif os.path.isdir(filepath):
        for child in os.listdir(filepath):
            get_all_child_files(os.path.join(filepath, child), outlog)


root1 = 'trial'
root2 = 'paywall'


filelist1 = []
filelist2 = []

get_all_child_files(root1, filelist1)
get_all_child_files(root2, filelist2)

relative_filelist1 = [os.path.relpath(f, root1) for f in filelist1]
relative_filelist2 = [os.path.relpath(f, root2) for f in filelist2]

for rel_path in relative_filelist1:
    if rel_path not in relative_filelist2:
        print('rel_path not in relative_filelist2', rel_path)
        continue

    abs_path1 = os.path.join(root1, rel_path)
    abs_path2 = os.path.join(root2, rel_path)
    file_content_bs1 = open(abs_path1, 'rb').read()
    file_content_bs2 = open(abs_path2, 'rb').read()
    if file_content_bs1 != file_content_bs2:
        print('The file is different:', rel_path)
        print_hexdump_side_by_side(file_content_bs1, file_content_bs2)
