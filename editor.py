#!/usr/bin/env python
"""Tools for invoking editors programmatically."""

from __future__ import print_function

import locale
import os.path
import subprocess
import tempfile


__all__ = [
    'edit',
    'get_editor',
    'EditorError',
]

__version__ = '0.4'


class EditorError(RuntimeError):
    pass


def get_editor():
    # Get the editor from the environment.  Prefer VISUAL to EDITOR
    editor = os.environ.get('VISUAL') or os.environ.get('EDITOR')
    if not editor:
        raise EditorError(
            "Unable to find a viable editor on this system."
            "Please set your $VISUAL and/or $EDITOR environment variable"
        )
    return editor


def edit(filename=None, contents=None):
    editor = get_editor()

    if filename is None:
        tmp = tempfile.NamedTemporaryFile()
        filename = tmp.name

    if contents is not None:
        with open(filename, mode='wb') as f:
            f.write(contents)

    cmd = '%s %s' % (editor, filename)

    proc = subprocess.Popen(cmd, close_fds=True, shell=True)
    proc.communicate()

    with open(filename, mode='rb') as f:
        return f.read()


def _get_editor(ns):
    print(get_editor())


def _edit(ns):
    contents = ns.contents
    if contents is not None:
        contents = contents.encode(locale.getpreferredencoding())
    print(edit(filename=ns.path, contents=contents))


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers()

    cmd = sp.add_parser('get-editor')
    cmd.set_defaults(cmd=_get_editor)

    cmd = sp.add_parser('edit')
    cmd.set_defaults(cmd=_edit)
    cmd.add_argument('path', type=str, nargs='?')
    cmd.add_argument('--contents', type=str)

    ns = ap.parse_args()
    ns.cmd(ns)
