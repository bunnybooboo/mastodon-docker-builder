#!/usr/bin/env python3

from datetime import datetime
import sys
import subprocess
from argparse import ArgumentParser

image_name = 'maastodon/mastodon-docker'
build_tag = '+maas.0.2.0'

aliases = {
    'latest': 'v2.3.3',
    'v2.3': 'v2.3.3',
    'v2.2': 'v2.2.0',
    'v2.1': 'v2.1.3',
    'v2.0': 'v2.0.0',
    'v1.6': 'v1.6.1',
    'v1.5': 'v1.5.1',
    'v1.4': 'v1.4.7',
}

builds = [
    # Image tag         # Mastodon tag      # Dockerfile name
    ('master',          'HEAD',             'Dockerfile-v2.3.0'),
    ('v2.3.3',          'v2.3.3',           'Dockerfile-v2.3.0'),
    ('v2.3.2',          'v2.3.2',           'Dockerfile-v2.3.0'),
    ('v2.3.1',          'v2.3.1',           'Dockerfile-v2.3.0'),
    ('v2.3.1-rc2',      'v2.3.1rc2',        'Dockerfile-v2.3.0'),
    ('v2.3.1-rc1',      'v2.3.1rc1',        'Dockerfile-v2.3.0'),
    ('v2.3.0',          'v2.3.0',           'Dockerfile-v2.3.0'),
    ('v2.3.0-rc3',      'v2.3.0rc3',        'Dockerfile-v2.3.0'),
    ('v2.3.0-rc2',      'v2.3.0rc2',        'Dockerfile-v2.3.0'),
    ('v2.3.0-rc1',      'v2.3.0rc1',        'Dockerfile-v2.3.0'),
    ('v2.2.0',          'v2.2.0',           'Dockerfile-v2.0.0'),
    ('v2.2.0-rc2',      'v2.2.0rc2',        'Dockerfile-v2.0.0'),
    ('v2.2.0-rc1',      'v2.2.0rc1',        'Dockerfile-v2.0.0'),
    ('v2.1.3',          'v2.1.3',           'Dockerfile-v2.0.0'),
    ('v2.1.2',          'v2.1.2',           'Dockerfile-v2.0.0'),
    ('v2.1.0',          'v2.1.0',           'Dockerfile-v2.0.0'),
    ('v2.1.0-rc3',      'v2.1.0rc3',        'Dockerfile-v2.0.0'),
    ('v2.0.0',          'v2.0.0',           'Dockerfile-v2.0.0'),
    ('v1.6.1',          'v1.6.1',           'Dockerfile-v1.6.1'),
    ('v1.6.0',          'v1.6.0',           'Dockerfile-v1.6.1'),
    ('v1.5.1',          'v1.5.1',           'Dockerfile-v1.6.1'),
    ('v1.5.0',          'v1.5.0',           'Dockerfile-v1.6.1'),
    ('v1.4.7',          'v1.4.7',           'Dockerfile-v1.6.1'),
]

def flat(l):
    for k in l:
        for m in k:
            yield m

def run(c, **kwargs):
    if isinstance(c, str):
        ct = c
    else:
        ct = " ".join(c)
    print("> " + ct)
    print(subprocess.run(c, **kwargs))


def get_build(q):
    q = aliases.get(q, q)
    for im_tag, src_tag, df in builds:
        if q == im_tag:
            return q, im_tag, src_tag, df
    else:
        print("%s unknown" % q)
        return


def make(q):
    q, im_tag, src_tag, df = get_build(q)

    names = [k for k, v in aliases.items() if v == q] + [q]
    args = []
    args.extend(flat((('-t', '%s:%s' % (image_name, t)) for t in names)))
    args.extend([
        '--build-arg', 'MASTODON_VERSION=' + src_tag,
        '--build-arg', 'IMAGE_VERSION=' + im_tag + build_tag,
    ])

    run(
        'git pull',
        cwd='./mastodon/',
        shell=True,
    )
    run(
        'git checkout %s' % src_tag,
        cwd='./mastodon/',
        shell=True,
        check=True,
    )
    run(
        ['docker', 'build', '-f', df] + args + ['.'],
        check=True,
    )


def push(q):
    q, im_tag, src_tag, df = get_build(q)

    names = [k for k, v in aliases.items() if v == q] + [q]
    for t in names:
        tag = '%s:%s' % (image_name, t)
        run(
            ['docker', 'push', tag],
            check=True,
        )


def main():
    global image_name

    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--build-all', action='store_true')
    group.add_argument('--build-one', action='store')
    parser.add_argument('--push', action='store_true')
    parser.add_argument('--image', action='store', default=image_name)

    args = parser.parse_args()

    image_name = args.image

    if args.build_one:
        make(args.build_one)
        if args.push:
            push(args.build_one)
        return

    if args.build_all:
        for v, _, _ in builds:
            make(v)
        if args.push:
            for v, _, _ in builds:
                push(v)
        return

    print("Nothing to do.")


if __name__ == '__main__':
    main()



