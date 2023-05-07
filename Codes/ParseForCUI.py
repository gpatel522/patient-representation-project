import os

input_directory = 'D:/outputFromCtakes'
output_directory = r'..\data\MimicIII\Patients\Cuis'

def read_cuis(file_name):
    """Return file as a list of CUIs"""
    infile = os.path.join(input_directory, file_name)
    text = open(infile).read()
    tokens = set()
    for token in text.split():
        if token.startswith("cui="):
            cleanedToken = token.replace("\"", "")
            tokens.add(cleanedToken.split("=")[1])
    return tokens


def write_cuis(lines, output_file, output_directory):
    print(lines)
    outfile = open(os.path.join(output_directory, output_file), 'w')
    for line in lines:
        outfile.write('%s\n' % line)
    outfile.close()


if __name__ == "__main__":
    for file_name in os.listdir(input_directory):
        print('file_name*-', file_name)
        cuis = read_cuis(file_name)
        write_cuis(cuis, file_name.split(".")[0]+".txt", output_directory)
