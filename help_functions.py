import re, os, sys
from main import *


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_fasta_from_str(fasta_str):

    if fasta_str.find('>') == -1:
        flash('The input file seems not in fasta format.')
        redirect(request.url)

    fasta_str = fasta_str.replace("\r", "")
    records = fasta_str.split('>')[1:]
    myFasta = []
    for fasta in records:
        array = fasta.split('\n')
        # print("array")
        # print(array)
        name, sequence = array[0].split()[0], re.sub('[^ARNDCQEGHILKMFPSTWYV-]', '-', ''.join(array[1:]).upper())
        sequence = sequence.replace("U", "T")
        myFasta.append([name, sequence])

    return myFasta

def read_fasta_from_file(file):

    if os.path.exists(file) == False:
        flash('Error: "' + file + '" does not exist.')
        redirect(request.url)

    with open(file) as f:
        records = f.read()

    myFasta = read_fasta_from_str(records)

    return myFasta