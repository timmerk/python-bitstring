**bitstring** is a pure Python module that makes the creation, manipulation and analysis of binary data as simple and natural as possible.

Bitstrings can be constructed from integers, floats, hex, octal, binary, bytes or files. They can also be created and interpreted using flexible format strings.

Bitstrings can be sliced, joined, reversed, inserted into, overwritten, etc. with simple methods or using slice notation. They can also be read from, searched and replaced, and navigated in, similar to a file or stream.

Internally the bit data is efficiently stored in byte arrays, the module has been optimized for speed, and excellent code coverage is given by over 300 unit tests.

The latest versions are available for Python 2.6 and later (including Python 3). For Python 2.4 / 2.5 you can still use version 1.0, but you should refer to the manual that comes with the bitstring 1.0 download as some of the information on this website isn't applicable to that version.

**To get updates on new releases you can [subscribe to the project on freshmeat](http://freshmeat.net/projects/python-bitstring).**

---

# News #

## <font color='#4444cc'>May 24th 2010:</font> <font color='green'>Version 2.0.0 beta 1 for Python 2.6 and 3.x released</font> ##

This is a major new release that breaks compatibility with previous versions in a number of areas, but mostly through the removal of some redundant methods. It is not a radical change from version 1.3, and new users are advised to start with version 2.0. Although it is a beta I don't expect any (or only minor) functional changes before 2.0 proper.

For details see the ReleaseNotes.

---

## <font color='#4444cc'><a href='http://python-bitstring.googlecode.com/svn/tags/bitstring-1.3.0/doc/html/index.html'>View the Documentation Here</a></font> ##

It contains a walk-through of all the features and a complete reference section.


---


## <font color='#4444cc'>Examples</font> ##

See the [Wiki](Examples.md) and the [user manual](http://python-bitstring.googlecode.com/svn/tags/bitstring-1.3.0/doc/html/examples.html) for more examples.

Creation:
```
>>> a = BitString('0b00101')    # 5 bits long
>>> b = Bits(a_file_object)     # Treat file as array of bits.
>>> c = BitString('0xff, 0b101, 0o65, uint:6=22')   # Many initialisers joined together
>>> d = pack('intle:16, hex=a, 0b1', 100, a='0x34f') # Create using bit-wise pack function
>>> e = pack('<16h', *range(16))
```
Different interpretations, slicing and concatenation:
```
>>> a = Bits('0x1af')
>>> a.hex, a.bin, a.uint     # Different interpretations using properties
('0x1af', '0b000110101111', 431)
>>> a[10:3:-1].bin           # Slice with negative step
'0b1110101'
>>> 3*a + 'int:20=40'
Bits('0x1af1af1af00028')
```

Reading data sequentially.
```
>>> b = BitString('0x160120f')
>>> b.read('hex:12')           # Read 12 bits, and interpret as hex
'0x160'
>>> b.pos = 0
>>> b.read('uint:12')          # Read those same bits, but interpret as integer
352
>>> b.readlist('uint:12, bin:3')  # Multiple reads
[288, '0b111']
```

Searching, inserting and deleting:
```
>>> c = BitString('0b00010010010010001111')   # c.hex == '0x1248f'
>>> c.find('0x48')    # Note that found byte wasn't byte-aligned
True
>>> c.replace('0b001', '0xabc')  # Replace all 3-bit occurrences with 12-bits
>>> c.insert('0b0000')
>>> del c[4:12]
```