#!/usr/bin/env python
"""
Unit tests for the bitarray module.
"""

import unittest
import sys

sys.path.insert(0, '..')
import bitstring
from bitstring import BitArray

class All(unittest.TestCase):
    def testCreationFromUint(self):
        s = BitArray(uint=15, length=6)
        self.assertEqual(s.bin, '001111')
        s = BitArray(uint=0, length=1)
        self.assertEqual(s.bin, '0')
        s.uint = 1
        self.assertEqual(s.uint, 1)
        s = BitArray(length=8)
        s.uint = 0
        self.assertEqual(s.uint, 0)
        s.uint = 255
        self.assertEqual(s.uint, 255)
        self.assertEqual(s.len, 8)
        self.assertRaises(bitstring.CreationError, s._setuint, 256)

    def testCreationFromOct(self):
        s = BitArray(oct='7')
        self.assertEqual(s.oct, '7')
        self.assertEqual(s.bin, '111')
        s.append('0o1')
        self.assertEqual(s.bin, '111001')
        s.oct = '12345670'
        self.assertEqual(s.length, 24)
        self.assertEqual(s.bin, '001010011100101110111000')
        s = BitArray('0o123')
        self.assertEqual(s.oct, '123')


class NoPosAttribute(unittest.TestCase):
    def testReplace(self):
        s = BitArray('0b01')
        s.replace('0b1', '0b11')
        self.assertEqual(s, '0b011')

    def testDelete(self):
        s = BitArray('0b000000001')
        del s[-1:]
        self.assertEqual(s, '0b00000000')

    def testInsert(self):
        s = BitArray('0b00')
        s.insert('0xf', 1)
        self.assertEqual(s, '0b011110')

    def testInsertParameters(self):
        s = BitArray('0b111')
        self.assertRaises(TypeError, s.insert, '0x4')

    def testOverwrite(self):
        s = BitArray('0b01110')
        s.overwrite('0b000', 1)
        self.assertEqual(s, '0b00000')

    def testOverwriteParameters(self):
        s = BitArray('0b0000')
        self.assertRaises(TypeError, s.overwrite, '0b111')

    def testPrepend(self):
        s = BitArray('0b0')
        s.prepend([1])
        self.assertEqual(s, [1, 0])

    def testRol(self):
        s = BitArray('0b0001')
        s.rol(1)
        self.assertEqual(s, '0b0010')

    def testRor(self):
        s = BitArray('0b1000')
        s.ror(1)
        self.assertEqual(s, '0b0100')

    def testSetItem(self):
        s = BitArray('0b000100')
        s[4:5] = '0xf'
        self.assertEqual(s, '0b000111110')
        s[0:1] = [1]
        self.assertEqual(s, '0b100111110')


class Bugs(unittest.TestCase):
    def testAddingNonsense(self):
        a = BitArray([0])
        a += '0' # a uint of length 0 - so nothing gets added.
        self.assertEqual(a, [0])
        self.assertRaises(ValueError, a.__iadd__, '3')
        self.assertRaises(ValueError, a.__iadd__, 'se')
        self.assertRaises(ValueError, a.__iadd__, 'float:32')


class ByteAligned(unittest.TestCase):
    def testDefault(self, defaultbytealigned=bitstring.bytealigned):
        self.assertFalse(defaultbytealigned)

    def testChangingIt(self):
        bitstring.bytealigned = True
        self.assertTrue(bitstring.bytealigned)
        bitstring.bytealigned = False

    def testNotByteAligned(self):
        bitstring.bytealigned = False
        a = BitArray('0x00 ff 0f f')
        l = list(a.findall('0xff'))
        self.assertEqual(l, [8, 20])
        p = a.find('0x0f')[0]
        self.assertEqual(p, 4)
        p = a.rfind('0xff')[0]
        self.assertEqual(p, 20)
        s = list(a.split('0xff'))
        self.assertEqual(s, ['0x00', '0xff0', '0xff'])
        a.replace('0xff', '')
        self.assertEqual(a, '0x000')

    # TODO
#    def testByteAligned(self):
#        bitstring.bytealigned = True
#        a = BitArray('0x00 ff 0f f')
#        l = list(a.findall('0xff'))
#        self.assertEqual(l, [8])
#        p = a.find('0x0f')[0]
#        self.assertEqual(p, 16)
#        p = a.rfind('0xff')[0]
#        self.assertEqual(p, 8)
#        s = list(a.split('0xff'))
#        self.assertEqual(s, ['0x00', '0xff0ff'])
#        a.replace('0xff', '')
#        self.assertEqual(a, '0x000ff')


class SliceAssignment(unittest.TestCase):

    def testSliceAssignmentSingleBit(self):
        a = BitArray('0b000')
        a[2] = '0b1'
        self.assertEqual(a.bin, '001')
        a[0] = BitArray(bin='1')
        self.assertEqual(a.bin, '101')
        a[-1] = '0b0'
        self.assertEqual(a.bin, '100')
        a[-3] = '0b0'
        self.assertEqual(a.bin, '000')

    def testSliceAssignmentSingleBitErrors(self):
        a = BitArray('0b000')
        self.assertRaises(IndexError, a.__setitem__, -4, '0b1')
        self.assertRaises(IndexError, a.__setitem__, 3, '0b1')
        self.assertRaises(TypeError, a.__setitem__, 1, 1.3)

    def testSliceAssignmentMulipleBits(self):
        a = BitArray('0b0')
        a[0] = '0b110'
        self.assertEqual(a.bin, '110')
        a[0] = '0b000'
        self.assertEqual(a.bin, '00010')
        a[0:3] = '0b111'
        self.assertEqual(a.bin, '11110')
        a[-2:] = '0b011'
        self.assertEqual(a.bin, '111011')
        a[:] = '0x12345'
        self.assertEqual(a.hex, '12345')
        a[:] = ''
        self.assertFalse(a)

    def testSliceAssignmentMultipleBitsErrors(self):
        a = BitArray()
        self.assertRaises(IndexError, a.__setitem__, 0, '0b00')
        a += '0b1'
        a[0:2] = '0b11'
        self.assertEqual(a, '0b11')

    def testDelSliceStep(self):
        a = BitArray(bin='100111101001001110110100101')
        del a[::2]
        self.assertEqual(a.bin, '0110010101100')
        del a[3:9:3]
        self.assertEqual(a.bin, '01101101100')
        del a[2:7:1]
        self.assertEqual(a.bin, '011100')
        del a[::99]
        self.assertEqual(a.bin, '11100')
        del a[::1]
        self.assertEqual(a.bin, '')

    def testDelSliceNegativeStep(self):
        a= BitArray('0b0001011101101100100110000001')
        del a[5:23:-3]
        self.assertEqual(a.bin, '0001011101101100100110000001')
        del a[25:3:-3]
        self.assertEqual(a.bin, '00011101010000100001')
        del a[:6:-7]
        self.assertEqual(a.bin, '000111010100010000')
        del a[15::-2]
        self.assertEqual(a.bin, '0010000000')
        del a[::-1]
        self.assertEqual(a.bin, '')

    def testSetSliceStep(self):
        a = BitArray(bin='0000000000')
        a[::2] = '0b11111'
        self.assertEqual(a.bin, '1010101010')
        a[4:9:3] = [0, 0]
        self.assertEqual(a.bin, '1010001010')

    def testSetSliceErrors(self):
        a = BitArray(8)
        try:
            a[::3] = [1]
            self.assertTrue(false)
        except ValueError:
            pass
        