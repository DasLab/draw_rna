import os
import random, string
import re
from subprocess import Popen, PIPE, STDOUT, check_call

DEFAULT_TEMPERATURE = 37.0
DEFAULT_PARAMS = 'rna'
BASES = ['A','U','G','C']
BIN_DIR = "bin"
#fold a sequence
#@param seq:sequence
#@return: [parenthesis notation, energy]

def vienna_fold(seq, cotransc=False, constraint=False):
    """
    folds sequence using Vienna

    args:
    seq is the sequence string

    returns:
    secondary structure
    """
    # run ViennaRNA
    if constraint:
        options = "-C"
        input = seq + "\n" + constraint
    else:
        options = ""
        input = ''.join(seq)
    if cotransc:
        p = Popen([os.path.join(BIN_DIR,'CoFold'), '--distAlpha', '0.5', '--distTau', '640', '--noPS', options], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    elif '&' in seq:
        p = Popen([os.path.join(BIN_DIR,'RNAcofold'), '-T','37.0', '-noPS', options], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    else:
        p = Popen([os.path.join(BIN_DIR,'RNAfold'), '-T','37.0', '-noPS', options], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    pair= p.communicate(input=input)[0]
    p.wait()

    # split result by whitespace
    toks = re.split('\s+| \(?\s?',pair)
    ret= []
    ret.append(toks[1])
    ret.append(toks[2][1:-1])
    return ret

def nupack_fold(seq, oligo_conc, bpp = False):
    """
    folds sequence using nupack
    """
    os.system("source ~/.bashrc")
    rand_string = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
    split = seq.split("&")
    with open("%s.in" % rand_string, "w") as f:
        f.write("%s\n" % len(split))
        for seq in split:
            f.write("%s\n" % seq)
        f.write("1\n")
    os.system("cp %s/%s.list %s.list" % (BIN_DIR, len(split), rand_string))
    with open("%s.con" % rand_string, "w") as f:
        f.write("%s\n" % oligo_conc * (len(split)-1))
        f.write("1e-9\n")
    options = ['-material', DEFAULT_PARAMS, '-ordered', '-mfe']#, '-quiet']
    if bpp:
        options.append('-pairs')
    p = Popen([os.path.join(BIN_DIR,'complexes')] + options + [rand_string], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    p.wait()
    p = Popen([os.path.join(BIN_DIR,'concentrations'), '-ordered', rand_string], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    p.wait()
    # get mfe
    with open("%s.eq" % rand_string) as f_eq:
        for line in f_eq:
            if not line.startswith("%"):
                mfe = line.strip().split()
                if int(mfe[-3]):
                    break
    # get strand ordering
    with open("%s.ocx-key" % rand_string) as f_key:
        for line in f_key:
            if line.startswith("%s\t%s" % (mfe[0], mfe[1])):
                strands = [int(x) for x in line.strip().split()[2:]]
                break
    # get mfe structure
    with open("%s.ocx-mfe" % rand_string) as f_mfe:
        line = f_mfe.readline()
        while line:
            if line.startswith("%% complex%s-order%s" % (mfe[0], mfe[1])):
                f_mfe.readline()
                energy = f_mfe.readline().strip()
                secstruct = f_mfe.readline().strip()
                break
            line = f_mfe.readline()

    if bpp:
        bpp_matrix = []
        with open("%s.cx-epairs" % rand_string) as f_pairs:
            line = f_pairs.readline()
            while line:
                if line.startswith("%% complex%s" % complex[0]):
                    f_pairs.readline()
                    line = f_pairs.readline()
                    while not line.startswith("%"):
                        bpp_matrix.append(line.strip().split())
                line = f_mfe.readline()
        os.system("rm %s*" % rand_string)
        return bpp_matrix

    # get full secondary structure
    for i in range(len(split)):
        if i+1 not in strands:
            secstruct += "&" + "."*len(split[i])
            strands.append(i+1)
    os.system("rm %s*" % rand_string)
    return [secstruct.replace("+", "&"), energy, strands]

