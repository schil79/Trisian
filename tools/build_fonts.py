#!/usr/bin/env python3
"""Builds the web fonts in site/assets/fonts from the supplied font files.
Graphik (OTF) -> subset woff2, Latin only.
Archivo (variable TTF) -> one static instance, Condensed Black, subset to Basic Latin. Used for one word only.
Usage: python3 tools/build_fonts.py <graphik_dir> <archivo_variable.ttf>
"""
import sys, os
from fontTools.ttLib import TTFont
from fontTools import subset
from fontTools.varLib import instancer

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = os.path.join(root, 'site', 'assets', 'fonts')
os.makedirs(out, exist_ok=True)
gdir, arch = sys.argv[1], sys.argv[2]
UNI = 'U+0020-007E,U+00A0-00FF,U+2013,U+2014,U+2018,U+2019,U+201C,U+201D,U+2022,U+2026,U+2192,U+00D7'

def sub(src_font, dst):
    opts = subset.Options(); opts.flavor = 'woff2'; opts.layout_features = ['*']; opts.notdef_outline = True
    s = subset.Subsetter(opts); s.populate(unicodes=subset.parse_unicodes(UNI)); s.subset(src_font)
    src_font.flavor = 'woff2'; src_font.save(dst)
    print(os.path.basename(dst), os.path.getsize(dst) // 1024, 'KB')

for name in ['Light', 'Regular', 'Medium', 'Semibold', 'Bold']:
    sub(TTFont(os.path.join(gdir, f'Graphik-{name}.otf')), os.path.join(out, f'Graphik-{name}.woff2'))
vf = TTFont(arch)
inst = instancer.instantiateVariableFont(vf, {'wght': 900, 'wdth': 62})
sub(inst, os.path.join(out, 'Archivo-CondensedBlack.woff2'))
