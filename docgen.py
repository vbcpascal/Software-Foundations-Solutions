import sys
import os
from typing import *
import shutil

modules = [
    'Preface',
    'Basics',
    'Induction',
    'Lists',
    'Poly',
    'Tactics',
    'Logic',
    'IndProp',
    'ProofObjects',
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
    '(*CBE*)': '(** #</div><div class="warn"><div># *)',
    '(*CEE*)': '(** #</div></div><div class="doc"># *)',
    '(*CB-CMT*)': '(** #</div><div class="mycomment"><div># *)',
    '(*CE-CMT*)': '(** #</div></div><div class="doc"># *)',
}


def build_module(module_name: str):
    cmd = COQC + ' -Q . LF ' + module_name + '.v'
    os.system(cmd)


def test_module(module_name: str):
    if module_name == 'Preface':
        return
    cmd = COQC + ' -Q . LF ' + module_name + 'Test.v'
    os.system(cmd)


def gen_doc(module_name: str):
    # read and rename file
    codefile = module_name + '.v'
    with open(codefile, 'r') as f:
        coq_code = f.read()
    tmp_file = 'tmp_' + module_name + '.v'
    os.rename(codefile, tmp_file)

    # Replace

    # replace cb and ce
    for key in REPLACER:
        coq_code = coq_code.replace(key, REPLACER[key])

    # dump the new file
    with open(codefile, 'w+') as f:
        f.write(coq_code)

    # generate doc
    doc_file = module_name + '.html'
    header = " --with-header " + HEADER
    footer = " --with-footer " + FOOTER
    title = " -t " + module_name
    flags = " --html --no-glob --no-index --no-lib-name --lib-subtitles "
    output = " -o " + doc_file
    cmd = COQDOC + header + footer + title + flags + output + " " + codefile
    os.system(cmd)

    # remove temp file
    os.rename(tmp_file, codefile)

    # I don't know how to generate the subtitle QWQ
    htmlfile = module_name + '.html'
    with open(htmlfile, 'r') as f:
        content = f.read()
    content = content.replace('RP_TITLE_RP', module_name)

    b_index = content.find('<h1 class="libtitle">') + 21
    e_index = content.find('</h1>', b_index)
    title_str = content[b_index: e_index]
    if ':' in title_str:
        c_index = title_str.find(':')
        main_title = title_str[:c_index]
        sub_title = title_str[c_index + 2:]
        content = content.replace(
            title_str, main_title + '<span class="subtitle">' + sub_title)

    with open(htmlfile, 'w+') as f:
        f.write(content)


if __name__ == '__main__':
    options = sys.argv[1:]
    do_all = 'all' in options

    if 'build' in options or do_all:
        for module in modules:
            print("\033[95m[ Begin to build %s ]\033[0m" % (module))
            build_module(module)

    if 'test' in options or do_all:
        for module in modules[1:]:
            print("\033[94m[ Begin to test %s ]\033[0m" % (module))
            test_module(module)

    if 'doc' in options or do_all:
        for module in modules:
            print("\033[96m[ Begin to generate html of %s ]\033[0m" % (module))
            gen_doc(module)
