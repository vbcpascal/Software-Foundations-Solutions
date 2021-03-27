import sys
import os
from typing import *

modules = [
    'Preface',
    'Basics',
    'Induction',
    'Lists',
    'Poly',
]

COQC = 'coqc'
COQDOC = 'coqdoc'
HEADER = 'common/html/header.html'
FOOTER = 'common/html/footer.html'

REPLACER = {
    '(*CB*)': '(** #</div><div class="solution"><div># *)',
    '(*CE*)': '(** #</div></div><div class="doc"># *)',
    '(*CBL*)': '(** #</div><div class="solution-lemma"><div># *)',
    '(*CEL*)': '(** #</div></div><div class="doc"># *)',
}


def build_module(module_name: str):
    cmd = COQC + ' -Q . LF ' + module_name + '.v'
    os.system(cmd)


def gen_doc(module_name: str):
    # readfile
    codefile = module_name + '.v'
    with open(codefile, 'r') as f:
        coq_code = f.read()

    # replace cb and ce
    for key in REPLACER:
        coq_code = coq_code.replace(key, REPLACER[key])

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
    options = sys.argv[1:]
    do_all = 'all' in options

    if 'build' in options or do_all:
        for module in modules:
            build_module(module)

    if 'doc' in options or do_all:
        for module in modules:
            gen_doc(module)
