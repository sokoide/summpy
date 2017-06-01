#!/usr/bin/env python

import codecs
import pypandoc


f = codecs.open('README.rst', 'w', encoding='utf-8')
f.write(pypandoc.convert('README.md', 'rst'))
f.close()
