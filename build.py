#!/usr/bin/env python3

import glob
import json
import os
import subprocess


def ensure_dir(dirpath):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)


def extract_prelude(filepath):
    prelude = ''
    with open(filepath, 'r') as f:
        for line in f:
            if line == '\n':
                break

            prelude += line.split('//')[1]

    return prelude


def build_test(filepath, outdir):
    dirname = os.path.dirname(filepath)
    ensure_dir(os.path.join(outdir, dirname))

    basename, ext = os.path.splitext(filepath)

    if ext == '.c':
        subprocess.check_call([
            'clang',
            '-target',
            'wasm32-wasi',
            '-o',
            os.path.join(outdir, basename + '.wasm'),
            filepath,
        ])
    elif ext == '.rs':
        subprocess.check_call([
            'rustc',
            '--target',
            'wasm32-wasi',
            '-o',
            os.path.join(outdir, basename + '.wasm'),
            filepath,
        ])
    else:
        raise ValueError('Invalid source format')

    config = json.loads(extract_prelude(filepath))
    with open(os.path.join(outdir, basename + '.json'), 'w') as f:
        f.write(json.dumps(config, sort_keys=True, indent=2))
        f.write('\n')

def main():
    for filepath in glob.iglob('integration/*.*'):
        build_test(filepath, "build")

if __name__ == '__main__':
    main()
