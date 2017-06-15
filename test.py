from diff import *
diff_1=DiffCommands('diff_1.txt')
print(diff_1)

diff_2=DiffCommands('diff_2.txt')
print(diff_2)


diff_3=DiffCommands('diff_3.txt')
print(diff_3)

pair_of_files = OriginalNewFiles('file_1_1.txt', 'file_1_2.txt')
pair_of_files.is_a_possible_diff(diff_1)
pair_of_files.is_a_possible_diff(diff_2)
pair_of_files.is_a_possible_diff(diff_3)

pair_of_files.output_diff(diff_1)

pair_of_files.output_unmodified_from_original(diff_1)

pair_of_files.output_unmodified_from_new(diff_1)

pair_of_files.get_all_diff_commands()

diffs = pair_of_files.get_all_diff_commands()

len(diffs)
print(diffs[0])

pair_of_files = OriginalNewFiles('file_1_2.txt', 'file_1_1.txt')
diffs = pair_of_files.get_all_diff_commands()
len(diffs)

print(diffs[0])


pair_of_files = OriginalNewFiles('file_1_1.txt', 'file_1_1.txt')
diffs = pair_of_files.get_all_diff_commands()
len(diffs)
print(diffs[0])

pair_of_files = OriginalNewFiles('file_2_1.txt', 'file_2_2.txt')

pair_of_files.is_a_possible_diff(diff_1)

pair_of_files.is_a_possible_diff(diff_2)

pair_of_files.is_a_possible_diff(diff_3)

pair_of_files.output_diff(diff_2)


pair_of_files.output_unmodified_from_original(diff_2)
pair_of_files.output_unmodified_from_new(diff_2)
diffs = pair_of_files.get_all_diff_commands()
len(diffs)
print(diffs[0])
print(diffs[1])
pair_of_files = OriginalNewFiles('file_2_2.txt', 'file_2_1.txt')
diffs = pair_of_files.get_all_diff_commands()

len(diffs)

print(diffs[0])
print(diffs[1])
pair_of_files = OriginalNewFiles('file_3_1.txt', 'file_3_2.txt')
pair_of_files.is_a_possible_diff(diff_1)
pair_of_files.is_a_possible_diff(diff_2)
pair_of_files.is_a_possible_diff(diff_3)

pair_of_files.output_diff(diff_3)

pair_of_files.output_unmodified_from_original(diff_3)

pair_of_files.output_unmodified_from_new(diff_3)
diffs = pair_of_files.get_all_diff_commands()

len(diffs)

print(diffs[0])
print(diffs[1])
print(diffs[2])

pair_of_files = OriginalNewFiles('file_3_2.txt', 'file_3_1.txt')
diffs = pair_of_files.get_all_diff_commands()
len(diffs)

print(diffs[0])
print(diffs[1])
print(diffs[2])

