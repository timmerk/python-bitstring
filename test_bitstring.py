#!/usr/bin/env python
"""
Unit tests for the bitstring module.
http://python-bitstring.googlecode.com
"""

license = """
The MIT License

Copyright (c) 2006-2009 Scott Griffiths (scott@griffiths.name)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import unittest
import bitstring
import copy
from bitstring import BitString, BitStringError


class BitStringTest(unittest.TestCase):
    
    def testCreationFromFile(self):
        s = BitString(filename = 'test/test.m1v')
        self.assertEqual(s[0:32].hex, '0x000001b3')
        self.assertEqual(s.readbytes(4).hex, '0x000001b3')
        width = s.readbits(12).uint
        height = s.readbits(12).uint
        self.assertEqual((width, height), (352, 288))
    
    def testCreationFromFileOperations(self):
        s = BitString(filename='test/smalltestfile')
        s.append('0xff')
        self.assertEqual(s.hex, '0x0123456789abcdefff')
        
        s = BitString(filename='test/smalltestfile')
        t = BitString('0xff').append(s)
        self.assertEqual(t.hex, '0xff0123456789abcdef')
        
        s = BitString(filename='test/smalltestfile')
        s.deletebits(1, 0)
        self.assertEqual((BitString('0b0') + s).hex, '0x0123456789abcdef')
        
        s = BitString(filename='test/smalltestfile')
        s.deletebytes(7, 0)
        self.assertEqual(s.hex, '0xef')
        
        s = BitString(filename='test/smalltestfile')
        s.insert('0xc', 4)
        self.assertEqual(s.hex, '0x0c123456789abcdef')
        
        s = BitString(filename='test/smalltestfile')
        s.prepend('0xf')
        self.assertEqual(s.hex, '0xf0123456789abcdef')
        
        s = BitString(filename='test/smalltestfile')
        s.overwrite('0xaaa', 12)
        self.assertEqual(s.hex, '0x012aaa6789abcdef')
        
        s = BitString(filename='test/smalltestfile')
        s.reversebits()
        self.assertEquals(s.hex, '0xf7b3d591e6a2c480')
        
        s = BitString(filename='test/smalltestfile')
        s.truncateend(60)
        self.assertEqual(s.hex, '0x0')
        
        s = BitString(filename='test/smalltestfile')
        s.truncatestart(60)
        self.assertEqual(s.hex, '0xf')

    def testFileProperties(self):
        s = BitString(filename='test/smalltestfile')
        self.assertEqual(s.hex, '0x0123456789abcdef')
        self.assertEqual(s.uint, 81985529216486895)
        self.assertEqual(s.int, 81985529216486895)
        self.assertEqual(s.bin, '0b0000000100100011010001010110011110001001101010111100110111101111')
        self.assertEqual(s[:-1].oct, '0o002215053170465363367')
        s.bitpos = 0
        self.assertEqual(s.readse(), -72)
        s.bitpos = 0
        self.assertEqual(s.readue(), 144)
        self.assertEqual(s.data, '\x01\x23\x45\x67\x89\xab\xcd\xef')

    def testCreationFromFileWithLength(self):
        s = BitString(filename='test/test.m1v', length = 32)
        self.assertEqual(s.length, 32)
        self.assertEqual(s.hex, '0x000001b3')
        s = BitString(filename='test/test.m1v', length = 0)
        self.assertTrue(s.empty())
        self.assertRaises(ValueError, BitString, filename='test/test.m1v', length=999999999999)
    
    def testCreationFromFileWithOffset(self):
        self.assertRaises(ValueError, BitString, filename='test/test.m1v', offset=1)

    def testCreataionFromFileErrors(self):
        self.assertRaises(OSError, BitString, filename='Idonotexist')

    def testFindInFile(self):
        s = BitString(filename = 'test/test.m1v')
        self.assertTrue(s.findbytealigned('0x160120'))
        self.assertEqual(s.bytepos, 4)
        s3 = s.readbytes(3)
        self.assertEqual(s3.hex, '0x160120')
        s.bytepos = 0
        self.assertTrue(s._pos == 0)
        self.assertTrue(s.findbytealigned('0x0001b2'))
        self.assertEqual(s.bytepos, 13)

    def testHexFromFile(self):
        s = BitString(filename='test/test.m1v')
        self.assertEqual(s[0:32].hex, '0x000001b3')
        self.assertEqual(s[-32:].hex, '0x000001b7')
        s.hex = '0x11'
        self.assertEqual(s.hex, '0x11')

    def testFileOperations(self):
        s1 = BitString(filename='test/test.m1v')
        s2 = BitString(filename='test/test.m1v')
        self.assertEqual(s1.readbytes(4).hex, '0x000001b3')
        self.assertEqual(s2.readbytes(4).hex, '0x000001b3')
        s1.advancebytes(4)
        self.assertEqual(s1.readbyte().hex, '0x02')
        self.assertEqual(s2.readbytes(5).hex, '0x1601208302')
        s1.bitpos = s1.length
        self.assertRaises(ValueError, s1.advancebits, 1)

    def testVeryLargeFiles(self):
        # This uses an 11GB file which isn't distrubited for obvious reasons
        # and so these tests will fail for everyone except me!
        #s = BitString(filename='test/11GB.mkv')
        #self.assertEqual(s.length, 11743020505*8)
        #self.assertEqual(s[1000000000:1000000100].hex, '0xbdef7335d4545f680d669ce24')
        #self.assertEqual(s[-32:].hex, '0xbbebf7a1') # TODO: I haven't confirmed this is correct!
        #s.findbytealigned('0xff')
        pass

    def testFind1(self):
        s = BitString(bin='0b0000110110000')
        self.assertTrue(s.find(BitString(bin='11011')))
        self.assertEqual(s.bitpos, 4)
        self.assertEqual(s.readbits(5).bin, '0b11011')
        s.bitpos = 0
        self.assertFalse(s.find(BitString(bin='0b11001')))
    
    def testFind2(self):
        s = BitString(bin='0')
        self.assertTrue(s.find(s))
        self.assertEqual(s.bitpos, 0)
        self.assertFalse(s.find('0b00'))
        self.assertRaises(ValueError, s.find, BitString())

    def testFindWithOffset(self):
        s = BitString(hex='0x112233', offset = 4)
        self.assertTrue(s.find(BitString(hex='0x23')))
        self.assertEqual(s.bitpos, 8)

    def testFindCornerCases(self):
        s = BitString(bin='000111000111')
        self.assertTrue(s.find(BitString(bin='000')))
        self.assertEqual(s.bitpos, 0)
        self.assertTrue(s.find(BitString(bin='000')))
        self.assertEqual(s.bitpos, 0)
        self.assertTrue(s.find(BitString(bin='0111000111')))
        self.assertEqual(s.bitpos, 2)
        self.assertTrue(s.find(BitString(bin='000')))
        self.assertEqual(s.bitpos, 6)
        self.assertTrue(s.find(BitString(bin='111')))
        self.assertEqual(s.bitpos, 9)
        s.advancebits(2)
        self.assertTrue(s.find(BitString(bin='1'))) 

    def testCreationFromData(self):
        s = BitString(data='\xa0\xff')
        self.assertEqual((s.length, s.offset, s.hex), (16, 0, '0xa0ff'))

    def testCreationFromDataWithOffset(self):
        s1 = BitString(data='\x0b\x1c\x2f', offset=0, length=20)
        s2 = BitString(data='\xa0\xb1\xC2', offset=4)
        self.assertEqual((s2.length, s2.offset, s2.hex), (20, 4, '0x0b1c2'))
        self.assertEqual((s1.length, s1.offset, s1.hex), (20, 0, '0x0b1c2'))
        self.assertTrue(s1 == s2)

    def testCreationFromHex(self):
        s = BitString(hex='0xA0ff')
        self.assertEqual((s.length, s.offset, s.hex), (16, 0, '0xa0ff'))
        s = BitString(hex='0x0x0X')
        self.assertEqual((s.length, s.offset, s.hex), (0, 0, ''))

    def testCreationFromHexWithOffset(self):
        s = BitString(hex='0xa0b1c2', offset = 4)
        self.assertEqual((s.length, s.offset, s.hex), (20, 4, '0x0b1c2'))
    
    def testCreationFromHexWithWhitespace(self):
        s = BitString(hex='  \n0 X a  4e       \r3  \n')
        self.assertEqual(s.hex, '0xa4e3')
        
    def testCreationFromHexErrors(self):
        self.assertRaises(ValueError, BitString, hex='0xx0')
        self.assertRaises(ValueError, BitString, hex='0xX0')
        self.assertRaises(ValueError, BitString, hex='0Xx0')
        self.assertRaises(ValueError, BitString, hex='-2e')
        
    def testCreationFromBin(self):
        s = BitString(bin='1010000011111111')
        self.assertEqual((s.length, s.offset, s.hex), (16, 0, '0xa0ff'))
        self.assertEqual(s.bitpos, 0)
        s = BitString(bin='00', length=1)
        self.assertEqual(s.bin, '0b0')
        s = BitString(bin='00', length=0)
        self.assertEqual(s.bin, '')
        s = BitString(bin=' 0000 \n 0001\r ')
        self.assertEqual(s.bin, '0b00000001')

    def testCreationFromBinWithOffset(self):
        s = BitString(bin='0', offset=1)
        self.assertTrue(s.empty())
        s = BitString(bin='00111', offset=2)
        self.assertEqual(s.bin, '0b111')
        
    def testCreationFromBinWithWhitespace(self):
        s = BitString(bin='  \r\r\n0   B    00   1 1 \t0 ')
        self.assertEqual(s.bin, '0b00110')

    def testCreationFromUint(self):
        s = BitString(uint = 15, length = 6)
        self.assertEqual(s.bin, '0b001111')
        s = BitString(uint = 0, length = 1)
        self.assertEqual(s.bin, '0b0')
        s.uint = 1
        self.assertEqual(s.uint, 1)
        s = BitString(length = 8)
        s.uint = 0
        self.assertEqual(s.uint, 0)
        s.uint = 255
        self.assertEqual(s.uint, 255)
        self.assertRaises(ValueError, s._setuint, 256)

    def testCreationFromUintWithOffset(self):
        self.assertRaises(BitStringError, BitString, uint=12, length=8, offset=1)

    def testCreationFromUintErrors(self):
        self.assertRaises(ValueError, BitString, uint = -1, length = 10)
        self.assertRaises(ValueError, BitString, uint = 12)
        self.assertRaises(ValueError, BitString, uint = 4, length = 2)
        self.assertRaises(ValueError, BitString, uint = 0, length = 0)
        self.assertRaises(ValueError, BitString, uint = 12, length = -12)

    def testCreationFromInt(self):
        s = BitString(int = 0, length = 4)
        self.assertEqual(s.bin, '0b0000')
        s = BitString(int = 1, length = 2)
        self.assertEqual(s.bin, '0b01')
        s = BitString(int = -1, length = 11)
        self.assertEqual(s.bin, '0b11111111111')
        s = BitString(int = 12, length = 7)
        self.assertEqual(s.int, 12)
        s = BitString(int = -243, length = 108)
        self.assertEqual((s.int, s.length), (-243, 108))
        for length in range(6, 10):
            for value in range(-17, 17):
                s = BitString(int = value, length = length)
                self.assertEqual((s.int, s.length), (value, length))

    def testCreationFromIntWithOffset(self):
        self.assertRaises(BitStringError, BitString, int=12, length=8, offset=1)
    
    def testCreationFromIntErrors(self):
        self.assertRaises(ValueError, BitString, int = -1, length = 0)
        self.assertRaises(ValueError, BitString, int = 12)
        self.assertRaises(ValueError, BitString, int = 4, length = 3)
        self.assertRaises(ValueError, BitString, int = -5, length = 3)
    
    def testCreationFromSe(self):
        [self.assertEqual(BitString(se = i).se, i) for i in range(-10, 10)]

    def testCreationFromSeWithOffset(self):
        self.assertRaises(BitStringError, BitString, se=-13, offset=1)
    
    def testCreationFromSeErrors(self):
        self.assertRaises(BitStringError, BitString, se = -5, length = 33)
        s = BitString(bin='001000')
        self.assertRaises(BitStringError, s._getse)
    
    def testCreationFromUe(self):
        [self.assertEqual(BitString(ue=i).ue, i) for i in range(0, 20)]

    def testCreationFromUeWithOffset(self):
        self.assertRaises(BitStringError, BitString, ue=104, offset=2)

    def testCreationFromUeErrors(self):
        self.assertRaises(ValueError, BitString, ue = -1)
        self.assertRaises(BitStringError, BitString, ue = 1, length = 12)
        s = BitString(bin='10')
        self.assertRaises(BitStringError, s._getue)

    def testIncorrectBinAssignment(self):
        s = BitString()
        self.assertRaises(ValueError, s._setbin, '0010020')

    def testIncorrectHexAssignment(self):
        s = BitString()
        self.assertRaises(ValueError, s._sethexsafe, '0xabcdefg')

    def testLengthZero(self):
        self.assertEqual(BitString('').length, 0)

    def testLength(self):
        self.assertEqual(BitString('0x80').length, 8) 
        self.assertEqual(BitString('0x80', 5).length, 5)
        self.assertEqual(BitString('0x80', 0).length, 0)

    def testLengthErrors(self):
        self.assertRaises(ValueError, BitString, bin='111', length = -1)
        self.assertRaises(ValueError, BitString, bin='111', length = 4)

    def testOffsetLengthError(self):
        self.assertRaises(ValueError, BitString, 'hex=0xffff', offset = 8)
        self.assertRaises(ValueError, BitString, 'hex=0xffff', offset = -1)

    def testConvertToUint(self):
        self.assertEqual(BitString('0x10').uint, 16)
        self.assertEqual(BitString('0x1f', 6).uint, 7)

    def testConvertToInt(self):
        self.assertEqual(BitString('0x10').int, 16)
        self.assertEqual(BitString('0xf0', 5).int, -2)

    def testConvertToHex(self):
        self.assertEqual(BitString(data='\x00\x12\x23\xff').hex, '0x001223ff')

    def testConvertToBin(self):
        self.assertEqual(BitString('0x00',1).bin, '0b0')
        self.assertEqual(BitString('0x80',1).bin, '0b1')
        self.assertEqual(BitString(data='\x00\x12\x23\xff').bin, '0b00000000000100100010001111111111')

    def testReadBits(self):
        s = BitString(data='\x4d\x55')
        self.assertEqual(s.readbits(4).hex, '0x4')
        self.assertEqual(s.readbits(8).hex, '0xd5')
        self.assertEqual(s.readbits(1).bin, '0b0')
        self.assertEqual(s.readbits(3).bin, '0b101')
        self.assertEqual(s.readbits(0).empty(), True)

    def testReadByte(self):
        s = BitString(hex='4d55')
        self.assertEqual(s.readbyte().hex, '0x4d')
        self.assertEqual(s.readbyte().hex, '0x55')
    
    def testReadBytes(self):
        s = BitString(hex='0x112233448811')
        self.assertEqual(s.readbytes(3).hex, '0x112233')
        self.assertRaises(ValueError, s.readbytes, -2)
        s.bitpos += 1
        self.assertEqual(s.readbytes(2).bin, '0b1000100100010000')

    def testEmptyBitstring(self):
        s = BitString()
        self.assertRaises(ValueError, s.readbits, 1)
        self.assertEqual(s.bin, '')
        self.assertEqual(s.hex, '')
        self.assertRaises(ValueError, s._getint)
        self.assertRaises(ValueError, s._getuint)
        self.assertEqual(s.empty(), True)

    def testNonEmptyBitString(self):
        s = BitString(bin='0')
        self.assertEqual(s.empty(), False)

    def testReadUE(self):
        self.assertRaises(BitStringError, BitString('')._getue)
        # The numbers 0 to 8 as unsigned Exponential-Golomb codes
        s = BitString(bin='1 010 011 00100 00101 00110 00111 0001000 0001001')
        self.assertEqual(s.bitpos, 0)
        for i in range(9):
            self.assertEqual(s.readue(), i)
        self.assertRaises(BitStringError, s.readue)

    def testReadSE(self):
        s = BitString(bin='010 00110 0001010 0001000 00111')
        self.assertEqual(s.readse(), 1)
        self.assertEqual(s.readse(), 3)
        self.assertEqual(s.readse(), 5)
        self.assertEqual(s.readse(), 4)
        self.assertEqual(s.readse(), -3)

    def testBitPosition(self):
        s = BitString(data='\x00\x00\x00')
        self.assertEqual(s.bitpos, 0)
        s.readbits(5)
        self.assertEqual(s.bitpos, 5)
        s.bitpos = s.length
        self.assertRaises(ValueError, s.readbit)

    def testBytePosition(self):
        s = BitString(data='\x00\x00\x00')
        self.assertEqual(s.bytepos, 0)
        s.readbits(10)
        self.assertRaises(BitStringError, s._getbytepos)
        s.readbits(6)
        self.assertEqual(s.bytepos, 2)

    def testSeekToBit(self):
        s = BitString(data='\x00\x00\x00\x00\x00\x00')
        s.bitpos = 0
        self.assertEqual(s.bitpos, 0)
        self.assertRaises(ValueError, s._setbitpos, -1)
        self.assertRaises(ValueError, s._setbitpos, 6*8+1)
        s.bitpos = 6*8
        self.assertEqual(s.bitpos, 6*8)

    def testSeekToByte(self):
        s = BitString(data='\x00\x00\x00\x00\x00\xab')
        s.bytepos = 5
        self.assertEqual(s.readbits(8).hex, '0xab')

    def testAdvanceBitsAndBytes(self):
        s = BitString(data='\x00\x00\x00\x00\x00\x00\x00\x00')
        s.advancebits(5)
        self.assertEqual(s.bitpos, 5)
        s.advancebytes(2)
        self.assertEqual(s.bitpos, 2*8+5)
        s.retreatbytes(1)
        self.assertEqual(s.bitpos, 8+5)
        self.assertRaises(ValueError, s.advancebytes, -2)

    def testFindBytes(self):
        s = BitString('0x010203040102ff')
        self.assertFalse(s.findbytealigned('0x05'))
        self.assertTrue(s.findbytealigned('0x02'))
        self.assertEqual(s.readbytes(2).hex, '0x0203')
        self.assertTrue(s.findbytealigned('0x02'))
        s.readbit()
        self.assertFalse(s.findbytealigned('0x02'))
    
    def testFindBytesAlignedCornerCases(self):
        s = BitString('0xff')
        self.assertTrue(s.findbytealigned(s))
        self.assertFalse(s.findbytealigned(BitString(hex='0x12')))
        self.assertFalse(s.findbytealigned(BitString(hex='0xffff')))

    def testFindBytesBitpos(self):
        s = BitString(hex='0x1122334455')
        s.bitpos = 2
        s.findbytealigned('0x66')
        self.assertEqual(s.bitpos, 2)
        s.bitpos = 38
        s.findbytealigned('0x66')
        self.assertEqual(s.bitpos, 38)

    def testFindByteAligned(self):
        s = BitString(hex='0x12345678')
        self.assertTrue(s.findbytealigned(BitString(hex='0x56')))
        self.assertEqual(s.bytepos, 2)
        s.bitpos = 0
        self.assertFalse(s.findbytealigned(BitString(hex='0x45')))

    def testFindByteAlignedWithOffset(self):
        s = BitString(hex='0x112233', offset=4)
        self.assertTrue(s.findbytealigned(BitString(hex='0x23')))
        self.assertEqual(s.offset, 0)

    def testFindByteAlignedErrors(self):
        s = BitString(hex='0xffff')
        self.assertRaises(ValueError, s.findbytealigned, '')
        self.assertRaises(ValueError, s.findbytealigned, BitString())
        self.assertRaises(ValueError, s.findbytealigned, BitString(bin='00'))

    def testOffset1(self):
        s = BitString(data='\x00\x1b\x3f', offset=4)
        self.assertEqual(s.readbits(8).bin, '0b00000001')
        self.assertEqual(s.length, 20)

    def testOffset2(self):
        s1 = BitString(data='\xf1\x02\x04')
        s2 = BitString(data='\xf1\x02\x04', length=23)
        for i in [1,2,3,4,5,6,7,6,5,4,3,2,1,0,7,3,5,1,4]:
            s1._setoffset(i)
            self.assertEqual(s1.hex, '0xf10204')
            s2._setoffset(i)
            self.assertEqual(s2.bin, '0b11110001000000100000010')
        self.assertRaises(ValueError, s1._setoffset, -1)
        self.assertRaises(ValueError, s1._setoffset, 8)
    
    def testAppend(self):
        s1 = BitString('0x00', 5)
        s1.append(BitString('0xff', 1))
        self.assertEqual(s1.bin, '0b000001')
        self.assertEqual(BitString('0x0102').append(BitString('0x0304')).hex, '0x01020304')

    def testAppendSameBitstring(self):
        s1 = BitString('0xf0', 6)
        s1.append(s1)
        self.assertEqual(s1.bin, '0b111100111100')
    
    def testAppendWithOffset(self):
        s = BitString(data='\x28\x28', offset=1)
        s.append('0b0')
        self.assertEqual(s.hex, '0x5050')

    def testByteAlign(self):
        s = BitString(hex='0001ff23')
        s.bytealign()
        self.assertEqual(s.bytepos, 0)
        s.advancebits(11)
        s.bytealign()
        self.assertEqual(s.bytepos, 2)
        s.retreatbits(10)
        s.bytealign()
        self.assertEqual(s.bytepos, 1)

    def testByteAlignWithOffset(self):
        s = BitString(hex='0112233')
        s._setoffset(3)
        bitstoalign = s.bytealign()
        self.assertEqual(bitstoalign, 0)
        self.assertEqual(s.readbits(5).bin, '0b00001')

    def testInsertByteAligned(self):
        self.assertEqual(BitString('0x0011').insert(BitString('0x22'), 8).hex, '0x002211')
        s = BitString('0xff', 0).insert(BitString(bin='101'), 0) 
        self.assertEqual(s.bin, '0b101')        

    def testTruncateStart(self):
        s = BitString('0b1')
        s.truncatestart(1)
        self.assertTrue(s.empty())
        s = BitString(hex='1234')
        self.assertEqual(s.truncatestart(0).hex, '0x1234')
        self.assertEqual(s.truncatestart(4).hex, '0x234')
        s2 = s.truncatestart(9)
        self.assertEqual(s.bin, '0b100')
        self.assertEqual(s2.bin, '0b100')
        s3 = s2.truncatestart(2)
        self.assertEqual(s3.bin, '0b0')
        self.assertEqual(s2.bin, '0b0')
        self.assertEqual(s.bin, '0b0')
        self.assertEqual(s.length, 1)
        s.truncatestart(1)
        self.assertEqual(s.empty(), True)

    def testTruncateEnd(self):
        s = BitString('0b1')
        s.truncateend(1)
        self.assertTrue(s.empty())
        s = BitString(data='\x12\x34')
        self.assertEqual(s.truncateend(0).hex, '0x1234')
        self.assertEqual(s.truncateend(4).hex, '0x123')
        s.truncateend(9)
        self.assertEqual(s.bin, '0b000')
        s.truncateend(3)
        self.assertEqual(s.empty(), True)
    
    def testByteAlignedSlice(self):
        s = BitString(hex='0x123456')
        self.assertEqual(s.slice(8, 16).hex, '0x34')
        s = s.slice(8, 24)
        self.assertEqual(s.length, 16)
        self.assertEqual(s.hex, '0x3456')
        s = s.slice(0, 8)
        self.assertEqual(s.hex, '0x34')
        s.hex = '0x123456'
        self.assertEqual(s.slice(8, 24).slice(0, 8).hex, '0x34')
    
    def testSlice(self):
        s = BitString(bin='000001111100000')
        s1 = s.slice(0, 5)
        s2 = s.slice(5, 10)
        s3 = s.slice(10, 15)
        self.assertEqual(s1.bin, '0b00000')
        self.assertEqual(s2.bin, '0b11111')
        self.assertEqual(s3.bin, '0b00000')

    def testSliceErrors(self):
        s = BitString(hex = '0x123456')
        self.assertRaises(ValueError, s.slice, -1, 8)
        self.assertRaises(ValueError, s.slice, 0, 33)
        self.assertRaises(ValueError, s.slice, 7, 5)

    def testInsert(self):
        s1 = BitString(hex='0x123456')
        s2 = BitString(hex='0xff')
        s3 = s1.insert(s2, 8)
        self.assertEqual(s3.hex, '0x12ff3456')
        self.assertEqual(s1.hex, '0x12ff3456')

    def testInsertNull(self):
        s = BitString(hex='0x123').insert(BitString(), 3)
        self.assertEqual(s.hex, '0x123')

    def testInsertBits(self):
        one = BitString(bin='1')
        zero = BitString(bin='0')
        s = BitString(bin='00')
        s.insert(one, 0)
        self.assertEqual(s.bin, '0b100')
        s.insert(zero, 0)
        self.assertEqual(s.bin, '0b0100')
        s.insert(one, s.length)
        self.assertEqual(s.bin, '0b01001')
        s = s.insert(s, 2)
        self.assertEqual(s.bin, '0b0101001001')

    def testSetHex(self):
        s = BitString()
        s.hex = 'ff'
        self.assertEqual(s.hex, '0xff')
        s.hex = '0x010203045'
        self.assertEqual(s.hex, '0x010203045')
        self.assertRaises(ValueError, s._sethexsafe, '0x002g')
    
    def testSetHexWithLength(self):
        s = BitString(hex='0xffff', length = 9)
        self.assertEqual(s.bin, '0b111111111')
        s2 = s.slice(0, 4)
        self.assertEqual(s2.hex, '0xf')

    def testSetBin(self):
        s = BitString(bin="000101101")
        self.assertEqual(s.bin, '0b000101101')
        self.assertEqual(s.length, 9)
        self.assertEqual(s.offset, 0)
        s.bin = '0'
        self.assertEqual(s.bin, '0b0')
        self.assertEqual(s.length, 1)

    def testSetEmptyBin(self):
        s = BitString(hex='0x000001b3')
        s.bin = ''
        self.assertEqual(s.length, 0)
        self.assertEqual(s.bin, '')

    def testSetInvalidBin(self):
        s = BitString()
        self.assertRaises(ValueError, s._setbin, '00102')

    def testSingleByteFromHexString(self):
        for i in range(0, 16):
            s = BitString(data=bitstring._single_byte_from_hex_string('0' + hex(i)[2:]), length=8)
            self.assertEqual(s.hex[3:], hex(i)[2:])
        for i in range(16, 256):
            s = BitString(data=bitstring._single_byte_from_hex_string(hex(i)[2:]), length=8)
            self.assertEqual(s.hex, hex(i))

    def testHexStringFromSingleByte(self):
        self.assertEqual(bitstring._hex_string_from_single_byte('\x00'), '00')
        self.assertEqual(bitstring._hex_string_from_single_byte('\x01'), '01')
        self.assertEqual(bitstring._hex_string_from_single_byte('\x4e'), '4e')
        self.assertEqual(bitstring._hex_string_from_single_byte('\xff'), 'ff')

    def testAdding(self):
        s1 = BitString(hex = '0x0102')
        s2 = BitString(hex = '0x0304')
        s3 = s1 + s2
        self.assertEqual(s1.hex, '0x0102')
        self.assertEqual(s2.hex, '0x0304')
        self.assertEqual(s3.hex, '0x01020304')
        s3 += s1
        self.assertEqual(s3.hex, '0x010203040102')
        self.assertEqual(s2.slice(9,16).bin, '0b0000100')
        self.assertEqual(s1.slice(0, 9).bin, '0b000000010')
        s4 = BitString(bin='000000010', length=9) + \
             BitString(bin='0000100', length=7)
        self.assertEqual(s4.bin, '0b0000000100000100')
        s2p = s2.slice(9, 16)
        s1p = s1.slice(0, 9)
        s5p = s1p + s2p
        s5 = s1.slice(0, 9) + s2.slice(9, 16)
        self.assertEqual(s5.bin, '0b0000000100000100')

    def testMoreAdding(self):
        s = BitString(bin='00') + BitString(bin='') + BitString(bin='11')
        self.assertEqual(s.bin, '0b0011')

    def testAddingWithOffset(self):
        s = BitString(bin='000011111') + BitString(bin='1110001', offset=3)
        self.assertEqual(s.bin, '0b0000111110001')

    def testOverwriteBit(self):
        s = BitString(bin='0')
        s.overwrite(BitString(bin='1'), 0)
        self.assertEqual(s.bin, '0b1')

    def testOverwriteLimits(self):
        s = BitString(bin='0b11111')
        s1 = s.overwrite(BitString(bin='000'), 0)
        self.assertEqual(s1.bin, '0b00011')
        s2 = s.overwrite('0b000', 2)
        self.assertEqual(s2.bin, '0b00000')

    def testOverwriteNull(self):
        s = BitString(hex='342563fedec')
        s2 = BitString(s)
        s.overwrite(BitString(bin=''), 23)
        self.assertEqual(s.bin, s2.bin)

    def testOverwritePosition(self):
        s1 = BitString(hex='0123456')
        s2 = BitString(hex='ff')
        s1.bytepos = 1
        s1.overwrite(s2)
        self.assertEqual((s1.hex, s1.bytepos), ('0x01ff456', 2))

    def testOverwriteErrors(self):
        s = BitString(bin='11111')
        self.assertRaises(ValueError, s.overwrite, BitString(bin='1'), -1)
        self.assertRaises(ValueError, s.overwrite, BitString(bin='1'), 6)
        self.assertRaises(ValueError, s.overwrite, BitString(bin='11111'), 1)

    def testDeleteBits(self):
        s = BitString(bin='000111100000')
        s.bitpos = 4
        s.deletebits(4)
        self.assertEqual(s.bin, '0b00010000')
        
    def testDeleteBitsWithPosition(self):
        s = BitString(bin='000111100000')
        s.deletebits(4, 4)
        self.assertEqual(s.bin, '0b00010000')

    def testDeleteBitsErrors(self):
        s = BitString(bin='000111')
        self.assertRaises(ValueError, s.deletebits, -3)
        self.assertRaises(ValueError, s.deletebits, 7)

    def testDeleteBytes(self):
        s = BitString('0x00112233')
        s.deletebytes(0, 1)
        self.assertEqual(s.hex, '0x00112233')
        s.deletebytes(1, 1)
        self.assertEqual(s.hex, '0x002233')
        self.assertEqual(s.bytepos, 0)
        s.deletebytes(3)
        self.assertTrue(s.empty())

    def testGetItemWithPositivePosition(self):
        s = BitString(bin='0b1011')
        self.assertEqual(s[0].bin, '0b1')
        self.assertEqual(s[1].bin, '0b0')
        self.assertEqual(s[2].bin, '0b1')
        self.assertEqual(s[3].bin, '0b1')
        self.assertRaises(IndexError, s.__getitem__, 4)

    def testGetItemWithNegativePosition(self):
        s = BitString(bin='1011')
        self.assertEqual(s[-1].bin, '0b1')
        self.assertEqual(s[-2].bin, '0b1')
        self.assertEqual(s[-3].bin, '0b0')
        self.assertEqual(s[-4].bin, '0b1')
        self.assertRaises(IndexError, s.__getitem__, -5)

    def testSlicing(self):
        s = BitString(hex='0123456789')
        self.assertEqual(s[0:8].hex, '0x01')
        self.assertEqual(s[0:0].empty(), True)
        self.assertEqual(s[23:20].empty(), True)
        self.assertEqual(s[8:12].bin, '0b0010')

    def testNegativeSlicing(self):
        s = BitString(hex='0x012345678')
        self.assertEqual(s[:-8].hex, '0x0123456')
        self.assertEqual(s[-16:-8].hex, '0x56')
        self.assertEqual(s[-24:].hex, '0x345678')

    def testSlicingErrors(self):
        s = BitString(hex='0x012345')
        self.assertRaises(BitStringError, s.__getitem__, slice(0,10,2))

    def testLen(self):
        s = BitString()
        self.assertEqual(len(s), 0)
        s = s.append(BitString(bin='001'))
        self.assertEqual(len(s), 3)
    
    def testJoin(self):
        s1 = BitString(bin='0')
        s2 = BitString(bin='1')
        s3 = BitString(bin='000')
        s4 = BitString(bin='111')
        strings = [s1, s2, s1, s3, s4]
        s = bitstring.join(strings)
        self.assertEqual(s.bin, '0b010000111')

    def testJoin2(self):
        s1 = BitString(hex='00112233445566778899aabbccddeeff')
        s2 = BitString(bin='0b000011')
        bsl = [s1[0:32], s1[4:12], s2, s2, s2, s2]
        s = bitstring.join(bsl)
        self.assertEqual(s.hex, '0x00112233010c30c3')
                
        bsl = [BitString(uint=j, length=12) for j in range(10) for i in range(10)]
        s = bitstring.join(bsl)
        self.assertEqual(s.length, 1200)

    def testSplitByteAlignedCornerCases(self):
        s = BitString()
        bsl = s.splitbytealigned(BitString(hex='0xff'))
        self.assertEqual(bsl.next().hex, '')
        self.assertRaises(StopIteration, bsl.next)
        s = BitString(hex='aabbcceeddff')
        delimiter = BitString()
        # This next assert fails, but seems to be a Python bug?
        # self.assertRaises(BitStringError, s.split, delimiter)
        delimiter = BitString(hex='11')
        bsl = s.splitbytealigned(delimiter)
        self.assertEqual(bsl.next().hex, s.hex)

    def testSplitByteAligned(self):
        s = BitString(hex='0x1234aa1234bbcc1234ffff')
        delimiter = BitString(hex='1234')
        bsl = s.splitbytealigned(delimiter)
        self.assertEqual([b.hex for b in bsl], ['', '0x1234aa', '0x1234bbcc', '0x1234ffff'])

    def testSplitByteAlignedWithIntialBytes(self):
        s = BitString(hex='aa471234fedc43 47112233 47 4723 472314')
        delimiter = BitString(hex='47')
        s.findbytealigned(delimiter)
        self.assertEqual(s.bytepos, 1)
        bsl = s.splitbytealigned(delimiter)
        self.assertEqual([b.hex for b in bsl], ['0xaa', '0x471234fedc43', '0x47112233',
                                                  '0x47', '0x4723', '0x472314'])

    def testSplitByteAlignedWithOverlappingDelimiter(self):
        s = BitString(hex='aaffaaffaaffaaffaaff')
        bsl = s.splitbytealigned(BitString(hex='aaffaa'))
        self.assertEqual([b.hex for b in bsl], ['', '0xaaffaaff', '0xaaffaaffaaff'])

    def testPos(self):
        s = BitString(bin='1')
        self.assertEqual(s.bitpos, 0)
        s.readbits(1)
        self.assertEqual(s.bitpos, 1)

    def testWritingData(self):
        strings = [BitString(bin=x) for x in ['0','001','0011010010','010010','1011']]
        s = bitstring.join(strings)
        s2 = BitString(data = s.data)
        self.assertEqual(s2.bin, '0b000100110100100100101011')
        s2.append(BitString(bin='1'))
        s3 = BitString(data = s2.data)
        self.assertEqual(s3.bin, '0b00010011010010010010101110000000')
    
    def testWritingDataWithOffsets(self):
        s1 = BitString(data='\x10')
        s2 = BitString(data='\x08\x00', length=8, offset=1)
        s3 = BitString(data='\x04\x00', length=8, offset=2)
        self.assertTrue(s1 == s2)
        self.assertTrue(s2 == s3)
        self.assertTrue(s1.data == s2.data)
        self.assertTrue(s2.data == s3.data)

    def testVariousThings1(self):
        hexes = ['0x12345678', '0x87654321', '0xffffffffff', '0xed', '0x12ec']
        bins = ['0b001010', '0b1101011', '0b0010000100101110110110', '0b0', '0b011']
        bsl = []
        for (hex, bin) in zip(hexes, bins)*5:
            bsl.append(BitString(hex=hex))
            bsl.append(BitString(bin=bin))
        s = bitstring.join(bsl)
        for (hex, bin) in zip(hexes, bins)*5:
            h = s.readbytes((len(hex)-2)/2)
            b = s.readbits(len(bin)-2)
            self.assertEqual(h.hex, hex)
            self.assertEqual(b.bin, bin)

    def testVariousThings2(self):
        s1 = BitString(hex="0x1f08", length=13)
        self.assertEqual(s1.bin, '0b0001111100001')
        s2 = BitString(bin='0101011000', length=4)
        self.assertEqual(s2.bin, '0b0101')
        s3 = s1.append(s2)
        self.assertEqual(s3.length, 17)
        self.assertEqual(s3.bin, '0b00011111000010101')
        s3 = s3.slice(3,8)
        self.assertEqual(s3.bin, '0b11111')

    def testVariousThings3(self):
        s1 = BitString(hex='0x012480ff', length=25, offset=2)
        s2 = s1+s1
        self.assertEqual(s2.offset, 2)
        self.assertEqual(s2.length, 50)
        s3 = s2[0:25]
        s4 = s2[25:50]
        self.assertEqual(s3.bin, s4.bin)

    def testPeekBit(self):
        s = BitString(bin='01')
        self.assertEqual(s.peekbit().bin, '0b0')
        self.assertEqual(s.peekbit().bin, '0b0')
        self.assertEqual(s.readbit().bin, '0b0')
        self.assertEqual(s.peekbit().bin, '0b1')
        self.assertEqual(s.peekbit().bin, '0b1')

    def testPeekBits(self):
        s = BitString(data='\x1f', offset=3)
        self.assertEqual(s.length, 5)
        self.assertEqual(s.peekbits(5).bin, '0b11111')
        self.assertEqual(s.peekbits(5).bin, '0b11111')
        s.advancebits(1)
        self.assertRaises(ValueError, s.peekbits, 5)

    def testPeekByte(self):
        s = BitString(hex='001122334455')
        self.assertEqual(s.peekbyte().hex, '0x00')
        self.assertEqual(s.readbyte().hex, '0x00')
        s.bitpos += 33
        self.assertRaises(ValueError, s.peekbyte)
    
    def testPeekBytes(self):
        s = BitString(hex='001122334455')
        self.assertEqual(s.peekbytes(2).hex, '0x0011')
        self.assertEqual(s.readbytes(3).hex, '0x001122')
        self.assertEqual(s.peekbytes(3).hex, '0x334455')
        self.assertRaises(ValueError, s.peekbytes, 4)

    def testAdvanceBit(self):
        s = BitString(hex='0xff')
        s.bitpos = 6
        s.advancebit()
        self.assertEqual(s.bitpos, 7)
        s.advancebit()
        self.assertRaises(ValueError, s.advancebit)

    def testAdvanceByte(self):
        s = BitString(hex='0x010203')
        s.advancebyte()
        self.assertEqual(s.bytepos, 1)
        s.advancebyte()
        self.assertEqual(s.bytepos, 2)
        s.advancebyte()
        self.assertRaises(ValueError, s.advancebyte)
    
    def testRetreatBit(self):
        s = BitString(hex='0xff')
        self.assertRaises(ValueError, s.retreatbit)
        s.bitpos = 5
        s.retreatbit()
        self.assertEqual(s.bitpos, 4)

    def testRetreatByte(self):
        s = BitString(hex='0x010203')
        self.assertRaises(ValueError, s.retreatbyte)
        s.bytepos = 3
        s.retreatbyte()
        self.assertEqual(s.bytepos, 2)
        self.assertEqual(s.readbyte().hex, '0x03')
    
    def testPrint(self):
        for i in range(-3, 4):
            s = BitString(int = i, length=10)
            self.assertEqual(s.bin, s.__str__())
        s = BitString(hex='0x00')
        self.assertEqual(s.hex, s.__str__())
        s = BitString(filename='test/test.m1v')
        self.assertEqual(s[0:1024*8].hex+'...', s.__str__())

    def testCreationByAuto(self):
        s = BitString('0xff')
        self.assertEqual(s.hex, '0xff')
        s = BitString('0b00011')
        self.assertEqual(s.bin, '0b00011')
        self.assertRaises(ValueError, BitString, 'hello')

    def testInsertUsingAuto(self):
        s = BitString('0xff')
        s.insert('0x00', 4)
        self.assertEqual(s.hex, '0xf00f')
        self.assertRaises(ValueError, s.insert, 'ff')
    
    def testOverwriteUsingAuto(self):
        s = BitString('0x0110')
        s.overwrite('0b1')
        self.assertEqual(s.hex, '0x8110')
        s.overwrite('')
        self.assertEqual(s.hex, '0x8110')
        self.assertRaises(ValueError, s.overwrite, '0bf')

    def testFindUsingAuto(self):
        s = BitString('0b000000010100011000')
        self.assertTrue(s.find('0b101'))
        self.assertEqual(s.bitpos, 7)
    
    def testFindbytealignedUsingAuto(self):
        s = BitString('0x00004700')
        self.assertTrue(s.findbytealigned('0b01000111'))
        self.assertEqual(s.bytepos, 2)
    
    def testAppendUsingAuto(self):
        s = BitString('0b000')
        s2 = s.append('0b111')
        self.assertEqual(s.bin, '0b000111')
        self.assertEqual(s2.bin, '0b000111')
        s.append('0b0')
        self.assertEqual(s.bin, '0b0001110')
        self.assertEqual(s2.bin, '0b0001110')

    def testSplitByteAlignedUsingAuto(self):
        s = BitString('0x000143563200015533000123')
        sections = s.splitbytealigned('0x0001')
        self.assertEqual(sections.next().hex, '')
        self.assertEqual(sections.next().hex, '0x0001435632')
        self.assertEqual(sections.next().hex, '0x00015533')
        self.assertEqual(sections.next().hex, '0x000123')
        self.assertRaises(StopIteration, sections.next)

    def testSplitByteAlignedWithSelf(self):
        s = BitString('0x1234')
        sections = s.splitbytealigned(s)
        self.assertEqual(sections.next().hex, '')
        self.assertEqual(sections.next().hex, '0x1234')
        self.assertRaises(StopIteration, sections.next)
    
    def testPrepend(self):
        s = BitString('0b000')
        s2 = s.prepend('0b11')
        self.assertEquals(s.bin, '0b11000')
        self.assertEquals(s2.bin, '0b11000')
        s2.prepend(s2)
        self.assertEquals(s2.bin, '0b1100011000')
        self.assertEquals(s.bin, '0b1100011000')
    
    def testNullSlice(self):
        s = BitString('0x111')
        t = s.slice(1, 1)
        self.assertEqual(t._datastore.length(), 0)
        
    def testMultipleAutos(self):
        s = BitString('0xa').prepend('0xf').append('0xb')
        self.assertEqual(s.hex, '0xfab')
        s.prepend(s).append('0x100').overwrite('0x5', 4)
        self.assertEqual(s.hex, '0xf5bfab100')

    def testReverseBits(self):
        s = BitString('0b0011')
        s.reversebits()
        self.assertEqual(s.bin, '0b1100')
        s = BitString('0b10').reversebits()
        self.assertEqual(s.bin, '0b01')
        self.assertEqual(BitString().reversebits().bin, '')

    def testInitWithConcatenatedStrings(self):
        s = BitString('0xff 0Xee 0xd 0xcc')
        self.assertEqual(s.hex, '0xffeedcc')
        s = BitString('0b0 0B111 0b001')
        self.assertEqual(s.bin, '0b0111001')
        s += '0b1' + '0B1'
        self.assertEqual(s.bin, '0b011100111')
        s = BitString(hex='ff0xee')
        self.assertEqual(s.hex, '0xffee')
        s = BitString(bin='000b0b11')
        self.assertEqual(s.bin, '0b0011')
        s = BitString('  0o123 0O 7 0   o1')
        self.assertEqual(s.oct, '0o12371')
        s += '  0 o 332'
        self.assertEqual(s.oct, '0o12371332')
    
    def testInitialisationByOct(self):
        s = BitString(oct='7')
        self.assertEqual(s.oct, '0o7')
        self.assertEqual(s.bin, '0b111')
        s.append('0o1')
        self.assertEqual(s.bin, '0b111001')
        s.oct = '12345670'
        self.assertEqual(s.length, 24)
        self.assertEqual(s.bin, '0b001010011100101110111000')
        s = BitString('0o123')
        self.assertEqual(s.oct, '0o123')

    def testInitialisationByOctErrors(self):
        s = BitString('0b00011')
        self.assertRaises(ValueError, s._getoct)
        self.assertRaises(ValueError, s._setoct, '8')

    def testEquals(self):
        s1 = BitString('0b01010101')
        s2 = BitString('0b01010101')
        self.assertTrue(s1 == s2)
        s2._setoffset(4)
        self.assertTrue(s1 == s2)
        s3 = BitString()
        s4 = BitString()
        self.assertTrue(s3 == s4)
        self.assertFalse(s3 != s4)
        s5 = BitString(data='\xff', offset=2, length=3)
        s6 = BitString('0b111')
        self.assertTrue(s5 == s6)
    
    def testNotEquals(self):
        s1 = BitString('0b0')
        s2 = BitString('0b1')
        self.assertTrue(s1 != s2)
        self.assertFalse(s1 != BitString('0b0'))
    
    def testHexSpecialMethod(self):
        s1 = BitString('0xdeadbeef')
        self.assertEqual(hex(s1), s1.hex)
    
    def testOctSpecialMethod(self):
        s = BitString('0o77551')
        self.assertEqual(oct(s), s.oct)
    
    def testInvertSpecialMethod(self):
        s = BitString('0b00011001')
        self.assertEqual((~s).bin, '0b11100110')
        self.assertEqual((~BitString('0b0')).bin, '0b1')
        self.assertEqual((~BitString('0b1')).bin, '0b0')
        self.assertTrue(~~s == s)

    def testInvertSpecialMethodErrors(self):
        s = BitString()
        self.assertRaises(BitStringError, s.__invert__)

    def testShiftLeft(self):
        s = BitString('0b1010')
        t = s << 1
        self.assertEqual(s.bin, '0b1010')
        self.assertEqual(t.bin, '0b0100')
        t = t << 100
        self.assertEqual(t.bin, '0b0000')
    
    def testShiftLeftErrors(self):
        s = BitString()
        self.assertRaises(ValueError, s.__lshift__, 1)
        s = BitString('0xf')
        self.assertRaises(ValueError, s.__lshift__, -1)
    
    def testShiftRight(self):
        s = BitString('0b1010')
        t = s >> 1
        self.assertEqual(s.bin, '0b1010')
        self.assertEqual(t.bin, '0b0101')
        s = s >> 100
        self.assertEqual(s.bin, '0b0000')
    
    def testShiftRightErrors(self):
        s = BitString()
        self.assertRaises(ValueError, s.__rshift__, 1)
        s = BitString('0xf')
        self.assertRaises(ValueError, s.__rshift__, -1)

    def testShiftRightInPlace(self):
        s = BitString('0b11011')
        s >>= 2
        self.assertEqual(s.bin, '0b00110')
        s >>= 1000
        self.assertEqual(s.bin, '0b00000')
    
    def testShiftRightInPlaceErrors(self):
        s = BitString()
        self.assertRaises(ValueError, s.__irshift__, 1)
        s += '0b11'
        self.assertRaises(ValueError, s.__irshift__, -1)
    
    def testShiftLeftInPlace(self):
        s = BitString('0b11011')
        s <<= 2
        self.assertEqual(s.bin, '0b01100')
        s <<= 1000
        self.assertEqual(s.bin, '0b00000')
    
    def testShiftLeftInPlaceErrors(self):
        s = BitString()
        self.assertRaises(ValueError, s.__ilshift__, 1)
        s += '0b11'
        self.assertRaises(ValueError, s.__ilshift__, -1)

    def testMoreAdding(self):
        s = BitString('0x00')
        t = BitString('0x11')
        s += t
        self.assertEquals(s.hex, '0x0011')
        self.assertEquals(t.hex, '0x11')
        s += s
        self.assertEquals(s.hex, '0x00110011')
        
    def testJoinWithAuto(self):
        s = bitstring.join(['0xf', '0b00', BitString(bin='11')])
        self.assertEqual(s.bin, '0b11110011')

    def testAutoBitStringCopy(self):
        s = BitString('0xabcdef')
        t = BitString(s)
        self.assertEqual(hex(t), '0xabcdef')
        s.truncateend(8)
        self.assertEqual(hex(t), '0xabcdef')
        
    def testSliceAssignmentSingleBit(self):
        a = BitString('0b000')
        a[2] = '0b1'
        self.assertEqual(a.bin, '0b001')
        a[0] = BitString(bin='1')
        self.assertEqual(a.bin, '0b101')
        a[-1] = '0b0'
        self.assertEqual(a.bin, '0b100')
        a[-3] = '0b0'
        self.assertEqual(a.bin, '0b000')
    
    def testSliceAssignmentSingleBitErrors(self):
        a = BitString('0b000')
        self.assertRaises(IndexError, a.__setitem__, -4, '0b1')
        self.assertRaises(IndexError, a.__setitem__, 3, '0b1')
        self.assertRaises(TypeError, a.__setitem__, 1, 1)
        #self.assertRaises(IndexError, a.__setitem__, 2, '0b0')
    
    def testSliceAssignmentMulipleBits(self):
        a = BitString('0b0')
        a[0] = '0b110'
        self.assertEqual(a.bin, '0b110')
        a[0] = '0b000'
        self.assertEqual(a.bin, '0b00010')
        a[0:3] = '0b111'
        self.assertEqual(a.bin, '0b11110')
        a[-2:] = '0b011'
        self.assertEqual(a.bin, '0b111011')
        a[:] = '0x12345'
        self.assertEqual(a.hex, '0x12345')
        a[:] = ''
        self.assertTrue(a.empty())
    
    def testSliceAssignmentMultipleBitsErrors(self):
        a = BitString()
        self.assertRaises(IndexError, a.__setitem__, 0, '0b00')
        a += '0b1'
        self.assertRaises(IndexError, a.__setitem__, (0,2), '0b11')
    
    def testMultiplication(self):
        a = BitString('0xff')
        b = a*8
        self.assertEqual(b.hex, '0xffffffffffffffff')
        b = 4*a
        self.assertEqual(b.hex, '0xffffffff')
        self.assertTrue(1*a == a*1 == a)
        c = a*0
        self.assertTrue(c.empty())
        a *= 3
        self.assertEqual(a.hex, '0xffffff')
        a *= 0
        self.assertTrue(a.empty())
        one = BitString('0b1')
        zero = BitString('0b0')
        mix = one*2 + 3*zero + 2*one*2
        self.assertEqual(mix.bin, '0b110001111')
        q = BitString()
        q *= 143
        self.assertTrue(q.empty())

    def testMultiplicationErrors(self):
        a = BitString('0b1')
        b = BitString('0b0')
        self.assertRaises(ValueError, a.__mul__, -1)
        self.assertRaises(ValueError, a.__imul__, -1)
        self.assertRaises(ValueError, a.__rmul__, -1)
        self.assertRaises(TypeError, a.__mul__, 1.2)
        self.assertRaises(TypeError, a.__rmul__, b)
        self.assertRaises(TypeError, a.__imul__, b)
    
    def testEqualityWithAutoInitialised(self):
        a = BitString('0b00110111')
        self.assertTrue(a == '0b00110111')
        self.assertTrue(a == '0x37')
        self.assertTrue('0b0011 0111' == a)
        self.assertTrue('0x3 0x7' == a)
        self.assertFalse(a == '0b11001000')
        self.assertFalse('0x3737' == a)
    
    def testFileAndMemEquivalence(self):
        a = BitString(filename='test/smalltestfile')
        b = BitString(a)
        self.assertTrue(isinstance(a._datastore, bitstring._FileArray))
        self.assertTrue(isinstance(b._datastore, bitstring._MemArray))
        self.assertEqual(a._datastore[0], b._datastore[0])
        self.assertEqual(a._datastore[1:5], b._datastore[1:5])
    
    def testByte2Bits(self):
        for i in xrange(256):
            s = BitString(bin=bitstring._byte2bits[i])
            self.assertEqual(i, s.uint)
            self.assertEqual(s.length, 8)
    
    def testBitwiseAnd(self):
        a = BitString('0b01101')
        b = BitString('0b00110')
        self.assertEqual((a&b).bin, '0b00100')
        self.assertEqual((a&'0b11111'), a)
        self.assertRaises(ValueError, a.__and__, '0b1')
        self.assertRaises(ValueError, b.__and__, '0b110111111')
    
    def testBitwiseOr(self):
        a = BitString('0b111001001')
        b = BitString('0b011100011')
        self.assertEqual((a | b).bin, '0b111101011')
        self.assertEqual((a | '0b000000000'), a)
        self.assertRaises(ValueError, a.__or__, '0b0000')
        self.assertRaises(ValueError, b.__or__, a + '0b1')

    def testBitwiseXor(self):
        a = BitString('0b111001001')
        b = BitString('0b011100011')
        self.assertEqual((a ^ b).bin, '0b100101010')
        self.assertEqual((a ^ '0b111100000').bin, '0b000101001')
        self.assertRaises(ValueError, a.__xor__, '0b0000')
        self.assertRaises(ValueError, b.__xor__, a + '0b1')

    def testSeekBit(self):
        a = BitString('0b11111')
        a.seekbit(5)
        self.assertEqual(a.bitpos, 5)
        a.seekbit(0)
        self.assertEqual(a.bitpos, 0)
        self.assertRaises(ValueError, a.seekbit, -1)
        self.assertRaises(ValueError, a.seekbit, 6)
    
    def testSeekByte(self):
        a = BitString('0x1122334455')
        a.seekbyte(5)
        self.assertEqual(a.bytepos, 5)
        a.seekbyte(0)
        self.assertEqual(a.bytepos, 0)
        self.assertRaises(ValueError, a.seekbyte, -1)
        self.assertRaises(ValueError, a.seekbyte, 6)
    
    def testSplit(self):
        a = BitString('0b0 010100111 010100 0101 010')
        subs = [i.bin for i in a.split('0b010')]
        self.assertEqual(subs, ['0b0', '0b010100111', '0b010100', '0b0101', '0b010'])
    
    def testSplitCornerCases(self):
        a = BitString('0b000000')
        bsl = a.split('0b1')
        self.assertEqual(bsl.next(), a)
        self.assertRaises(StopIteration, bsl.next)
        b = BitString()
        bsl = b.split('0b001')
        self.assertTrue(bsl.next().empty())
        self.assertRaises(StopIteration, bsl.next)
        
    def testSplitErrors(self):
        a = BitString('0b0')
        #self.assertRaises(ValueError, a.split, '')
    
    def testPositionInSlice(self):
        a = BitString('0x00ffff00')
        a.bytepos = 2
        b = a[8:24]
        self.assertEqual(b.bytepos, 0)
    
    def testSliceWithOffset(self):
        a = BitString(data='\x00\xff\x00', offset=7)
        b = a.slice(7, 12)
        self.assertEqual(b.bin, '0b11000')
        

def main():
    unittest.main()

if __name__ == '__main__':
    main()