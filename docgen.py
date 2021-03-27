import sys
import os
from typing import *

modules = [
    'Basics',
    'Induction',
    'Lists',
]

COQDOC = 'coqdoc'
HEADER = 'common/html/header.html'
FOOTER = 'common/html/footer.html'

CBCODE = '(** #</div><div class="solution"><div># *)'
CECODE = '(** #</div></div><div class="doc"># *)'


def gen_doc(module_name: str):
    # readfile
    codefile = module_name + '.v'
    with open(codefile, 'r') as f:
        coq_code = f.read()

    # replace cb and ce
    coq_code = coq_code.replace("(*CB*)", CBCODE)
    coq_code = coq_code.replace("(*CE*)", CECODE)

    # dump a temp file
    tmp_file = 'tmp_' + module_name + '.v'
    with open(tmp_file, 'w+') as f:
        f.write(coq_code)

    # generate doc
    doc_file = module_name + '.html'
    header = " --with-header " + HEADER
    footer = " --with-footer " + FOOTER
    flags = " --html --no-glob --no-index "
    output = " -o " + doc_file
    cmd = COQDOC + header + footer + flags + output + " " + tmp_file
    os.system(cmd)

    # remove temp file
    os.remove(tmp_file)


if __name__ == '__main__':
    for module in modules:
        gen_doc(module)
