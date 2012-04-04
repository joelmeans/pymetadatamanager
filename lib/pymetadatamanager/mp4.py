############################################################################
#    Copyright (C) 2011 by Joel Means,,,                                   #
#    means.joel@gmail.com                                                  #
#                                                                          #
#    This program is free software; you can redistribute it and#or modify  #
#    it under the terms of the GNU General Public License as published by  #
#    the Free Software Foundation; either version 2 of the License, or     #
#    (at your option) any later version.                                   #
#                                                                          #
#    This program is distributed in the hope that it will be useful,       #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#    GNU General Public License for more details.                          #
#                                                                          #
#    You should have received a copy of the GNU General Public License     #
#    along with this program; if not, write to the                         #
#    Free Software Foundation, Inc.,                                       #
#    59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             #
############################################################################

__author__="jmeans"
__date__ ="$Apr 3, 2011 12:29:59 PM$"

import os
import logging
import struct
from PyQt4 import QtXml, QtCore

CHILD_ATOMS = ['ftyp', 'mdat', 'pdin', 'mfhd', 'tfhd', 'trun', 'tfra',
               'mfro', 'free', 'skip', 'uuid', 'mvhd', 'iods', 'drm ',
               'tkhd', 'clef', 'prof', 'enof', 'mdhd', 'hdlr', 'vmhd',
               'smhd', 'hmhd', 'nmhd', 'gmhd', 'url ', 'urn ',
               'alis', 'cios', 'stts', 'ctts', 'stsz', 'stz2',
               'stsc', 'stco', 'co64', 'stss', 'stsh', 'stdp', 'padb',
               'sdtp', 'sbgp', 'stps', 'elst', 'mehd', 'trex',
               'subs', 'xml ', 'bxml', 'iloc', 'pitm', 'infe',
               'frma', 'imif', 'schm', 'skcr', 'user', 'key ',
               'iviv', 'righ', 'name', 'priv', 'iKMS', 'iSFM', 'iSLT',
               'IKEY', 'hint', 'dpnd', 'ipir', 'mpod', 'sync', 'chap',
               'ipmc', 'tims', 'tsro', 'snro', 'srpp', 'rtp ', 'sdp ',
               'name', 'trpy', 'nump', 'tpyl', 'totl', 'npck', 'maxr',
               'dmed', 'dimm', 'drep', 'tmin', 'tmax', 'pmax', 'dmax',
               'payt', 'tpay', 'alac', 'avcC', 'damr', 'd263', 'dawp',
               'devc', 'dqcp', 'dsmv', 'bitr', 'btrt', 'm4ds', 'ftab',
               'ihdr', 'colr', 'fiel', 'jp2p', 'jsub', 'orfo', 'cprt',
               'cprt', 'titl', 'auth', 'perf', 'gnre', 'dcsp', 'albm',
               'yrrc', 'rtng', 'clsf', 'kywd', 'loci', 'ID32', 'tsel' 
               'data', 'esds', 'ac-3'
              ]

PARENT_ATOMS = ['moov', 'moof', 'traf', 'mfra', 'trak', 'tref', 'mdia',
                'tapt', 'minf', 'dinf', 'stbl', 'edts', 'udta', 'mvex',
                'ipro', 'sinf', 'hnti', 'hinf', 'jp2h', 'ilst', '----',
                'stik', 'trkn', 'disk', 'tmpo', 'cptr', 'cpil', 'covr',
                'rtng', 'pcst', 'catg', 'keyw', 'purl', 'egid', 'desc',
                'tvnn', 'tvsh', 'tven', 'tvsn', 'tves', 'purd', 'pgap',
                'meta', 'ldes', 'hdvd',
                '\xa9nam', '\xa9too', '\xa9alb', '\xa9art', '\xa9cmt',
                '\xa9gen', '\xa9day', '\xa9wrt', '\xa9grp', '\xa9lyr'
               ]
                
INTEGER_DATA_TYPES = ['tvsn', 'tves', 'hdvd', 'stik']

OFFSETS = {'meta':12, 'dref':16, 'iinf':14, 'stsd':16, 'schi':8,
           'mp4s':16, 'srtp':24, 'rtp ':24, 'alac':36, 'mp4a':36,
           'samr':36, 'sawb':36, 'sawp':36, 'sevc':36, 'sqcp':36,
           'ssmv':36, 'drms':36, 'tx3g':46, 'mjp2':86, 'mp4v':86,
           'avc1':86, 'jpeg':86, 's263':86, 'drmi':86
          }

STIKS = {0:'Movie', 
         1:'Normal',
         2:'Audiobook',
         5:'Whacked Bookmark',
         6:'Music Video',
         9:'Short Film',
        10:'TV Show',
        11:'Booklet'
        }

class MP4(object):
    """
    """
    def __init__(self, filename):
        self.logger = logging.getLogger('pymetadatamanager.mp4')
        self.file = open(filename, 'rb')
        self.atoms = QtXml.QDomDocument()
        self.root = self.atoms.createElement('atoms')
        self.atoms.appendChild(self.root)
        self._set_all_atoms()

    def __del__(self):
            pass

    def _read64(self, offset):
        self.file.seek(offset, os.SEEK_SET)
        data = self.file.read(8)
        if data is not None and len(data) == 8:
            return struct.unpack(">Q", data)[0]
        else:
            raise EOFError

    def _read32(self, offset):
        self.file.seek(offset, os.SEEK_SET)
        data = self.file.read(4)
        if data is not None and len(data) == 4:
            return struct.unpack(">L", data)[0]
        else:
            raise EOFError

    def _read16(self, offset):
        self.file.seek(offset, os.SEEK_SET)
        data = self.file.read(2)
        if data is not None and len(data) == 2:
            return struct.unpack(">H", data)[0]
        else:
            raise EOFError

    def _read8(self, offset):
        self.file.seek(offset, os.SEEK_SET)
        data = self.file.read(1)
        if data is not None and len(data) == 1:
            return struct.unpack(">B", data)[0]
        else:
            raise EOFError

    def _to_string64(self, data):
        a = (data >> 0)  & 0xff
        b = (data >> 8)  & 0xff
        c = (data >> 16) & 0xff
        d = (data >> 24) & 0xff
        e = (data >> 32) & 0xff
        f = (data >> 40) & 0xff
        g = (data >> 48) & 0xff
        h = (data >> 56) & 0xff
        return '%c%c%c%c%c%c%c%c' % (h, g, f, e, d, c, b, a)

    def _to_string32(self, data):
        a = (data >> 0)  & 0xff
        b = (data >> 8)  & 0xff
        c = (data >> 16) & 0xff
        d = (data >> 24) & 0xff
        return '%c%c%c%c' % (d, c, b, a)

    def _to_string16(self, data):
        a = (data >> 0)  & 0xff
        b = (data >> 8)  & 0xff
        return '%c%c' % (b, a)

    def _to_string8(self, data):
        a = (data >> 0)  & 0xff
        return '%c' % (a)

    def _parse_single_atom(self, offset):
        try:
            atom_size = self._read32(offset)
            offset += 4
            atom_type = self._to_string32(self._read32(offset))
            offset += 4
            if atom_size == 1:
               atom_size = self._read64(offset)
            if atom_size == 0:
                return None
            return self._make_atom_element(atom_size, atom_type, offset - 8)
        except EOFError:
            return None

    def _parse_multiple_atoms(self, offset, max_offset):
        atoms = []
        while offset < max_offset:
            atom = self._parse_single_atom(offset)
            if atom is not None:
                atoms.append(atom)
                offset += int(atom.attribute('size'))
        return atoms

    def _make_atom_element(self, size, type, offset):
        elem_atom = self.atoms.createElement(type)
        elem_atom.setAttribute('offset', offset)
        elem_atom.setAttribute('size', size)
        if type in PARENT_ATOMS or type in OFFSETS:
            if type in OFFSETS:
                buff = OFFSETS[type]
            else:
                buff = 8
            children = self._parse_multiple_atoms(offset + buff, offset + size)
            for child in children:
                if child.tagName() == 'data':
                    size = child.attribute('size')
                    offset = child.attribute('offset')
                    data = self._read_data_atom(size, offset, type)
                    text_data = self.atoms.createTextNode(data)
                    child.appendChild(text_data)
                if child.tagName() == 'name':
                    size = child.attribute('size')
                    offset = child.attribute('offset')
                    data = self._read_name_atom(size, offset, type)
                    text_data = self.atoms.createTextNode(data)
                    child.appendChild(text_data)
                elem_atom.appendChild(child)
        return elem_atom

    def _read_data_atom(self, size, offset, type):
        end_of_atom = int(size) + int(offset)
        pos = int(offset) + 16
        left = end_of_atom - pos
        data = ""
        if type == 'trkn':
            track_num = self._read16(pos + 2)
            total_tracks = self._read16(pos + 4)
            if total_tracks == 0:
                data = "%d" % (track_num,)
            else:
                data = "%d of %d" % (track_num, total_tracks)
            return data
        while pos < end_of_atom:
            if left >= 8:
                data64 = self._read64(pos)
                if type in INTEGER_DATA_TYPES:
                    data += str(data64)
                else:
                    data += self._to_string64(data64)
                pos += 8
            elif left >=4:
                data32 = self._read32(pos)
                if type in INTEGER_DATA_TYPES:
                    data += str(data32)
                else:
                    data += self._to_string32(data32)
                pos += 4
            elif left >=2:
                data16 = self._read16(pos)
                if type in INTEGER_DATA_TYPES:
                    data += str(data16)
                else:
                    data += self._to_string16(data16)
                pos += 2
            elif left == 1:
                data8 = self._read8(pos)
                if type in INTEGER_DATA_TYPES:
                    data += str(data8)
                else:
                    data += self._to_string8(data8)
                pos += 1
            left = end_of_atom - pos
        if type == 'stik':
            data = STIKS[int(data)]
        return data

    def _read_name_atom(self, size, offset, type):
        if type == '----':
            buff = 12
        else:
            buff = 8
        end_of_atom = int(size) + int(offset)
        pos = int(offset) + buff
        left = end_of_atom - pos
        data = ""
        while pos < end_of_atom:
            if left >= 8:
                data64 = self._read64(pos)
                data += self._to_string64(data64)
                pos += 8
            elif left >=4:
                data32 = self._read32(pos)
                data += self._to_string32(data32)
                pos += 4
            elif left >=2:
                data16 = self._read16(pos)
                data += self._to_string16(data16)
                pos += 2
            elif left == 1:
                data8 = self._read8(pos)
                data += self._to_string8(data8)
                pos += 1
            left = end_of_atom - pos
        return data

    def _set_all_atoms(self):
        offset = 0
        self.file.seek(0, os.SEEK_END)
        file_size = self.file.tell()
        atoms = self._parse_multiple_atoms(offset, file_size)
        for atom in atoms:
            self.root.appendChild(atom)

    def print_metadata(self):
        moov = self.root.firstChildElement('moov') 
        udta = moov.firstChildElement('udta')
        meta = udta.firstChildElement('meta')
        ilst = meta.firstChildElement('ilst')
        tags = ilst.childNodes()
        total_tags = tags.length()
        print "Total tags: %d" % (total_tags,)
        for i in range(0, total_tags):
            tag = tags.at(i)
            type = tag.toElement().tagName()
            data = tag.firstChildElement('data').text()
            print "%s = %s" % (type, data)
            
