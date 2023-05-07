import os

input_directory = '/Users/gpatel/Library/CloudStorage/Dropbox/Coursera/DL_in_Health/data/MimicIII/Patients/Cuis/'
output_directory = '/Users/gpatel/Library/CloudStorage/Dropbox/Coursera/DL_in_Health/data/MimicIII/Patients/'

cui_set = set()

def read_cuis(file_name):
    """Return file as a list of CUIs"""
    infile = os.path.join(input_directory, file_name)
    text = open(infile).read()
    for token in text.split():
        cui_set.add(token)


def write_cuis(lines, output_file, output_directory):
    #print(lines)
    outfile = open(os.path.join(output_directory, output_file), 'w')
    for line in lines:
        outfile.write('%s\n' % line)
    outfile.close()


if __name__ == "__main__":
    for file_name in os.listdir(input_directory):
        print('file_name*-', file_name)
        cuis = read_cuis(file_name)
    write_cuis(sorted(cui_set), "mimic-cuis.txt", output_directory)
