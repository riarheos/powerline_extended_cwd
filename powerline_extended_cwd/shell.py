from __future__ import (unicode_literals, division, absolute_import, print_function)

from powerline.theme import requires_segment_info
from powerline.segments.common.env import CwdSegment
from powerline.lib.unicode import out_u
import os
import yaml
import socket


@requires_segment_info
class ShellCwdSegment(CwdSegment):

    @staticmethod
    def get_cwd(segment_info):
        try:
            return out_u(segment_info['getcwd']())
        except OSError as e:
            return '[not found]'

    @staticmethod
    def xterm_header_segment(segment_info, cwd):
        if segment_info['environ'].get('SSH_CLIENT'):
            text = socket.gethostname() + ': ' + cwd
        else:
            text = cwd
        return { 'literal_contents': (0, '\[\033]0;%s\007\033]6;1;bg;*;default\a\]' % text) }

    @staticmethod
    def regular_segment(text, color=None):
        if color:
            return { 'contents': text, 'highlight_groups': [color, 'stash'] }
        else:
            return { 'contents': text }

    def substitute(self, segment_info, cwd, path, replacement, color):
        cwd = cwd[len(path) + 1:]
        if cwd:
            return [
                self.xterm_header_segment(segment_info, '{}/{}'.format(replacement, cwd)),
                self.regular_segment(replacement, color),
                self.regular_segment(cwd),
            ]

        return [ self.xterm_header_segment(segment_info, replacement), self.regular_segment(replacement, color) ]

    def __call__(self, pl, segment_info, shrink=[], **kwargs):
        cwd = self.get_cwd(segment_info)
        home = segment_info['home']

        # no home => nothing to shrink
        if not home:
            return [self.xterm_header_segment(segment_info, cwd), self.regular_segment(cwd)]

        # check if path is in the config
        for item in shrink:
            path = item[0].replace('~', home)
            if cwd.startswith(path):
                return self.substitute(segment_info, cwd, path, item[1], 'cwd:split')

        # finally the non-configured home
        if cwd.startswith(home):
            return self.substitute(segment_info, cwd, home, '~', 'cwd:home')

        return [self.xterm_header_segment(segment_info, cwd), self.regular_segment(cwd)]

cwd = ShellCwdSegment()
