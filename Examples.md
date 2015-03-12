
```
>>> from bitstring import BitStream, BitArray
```
### Creating bitstring ###

There are many ways to create and modify bitstrings, but no matter how they are created they are always internally stored as byte arrays. To create from hexadecimal, octal and binary strings use:
```
>>> h = BitArray(hex='000001b3')
>>> o = BitArray(oct='755')
>>> b = BitArray(bin='001001111')
```
Even better, you can use hex, oct and bin with automatic interpretation by prefixing with '0b', '0o' or '0x'
```
>>> h = BitArray('0x000001b3')
>>> o = BitArray('0o755')
>>> b = BitArray('0b001001111')
```
If you want to initialise from an ordinary Python string (read from a binary file, for example) then use the `bytes` initialiser.
```
>>> d = BitArray(bytes=b'\x03\xff\x23')
```
or you can initialise with a filename - the file will only read as necessary if you use a 'Const' class:
```
>>> f = Bits(filename='ABigFile.ext')
```
With integers the length of the bitstring in bits needs to be supplied. It must be long enough to contain the integer.
```
>>> ui = BitArray(uint=15, length=6)
```
or equivalently
```
>>> ui = BitArray('uint:6=15')
```

You can also combine the different methods to join sections together:
```
>>> s = BitArray('0xfe, 0b110, int:12=100, 0o7')
```

### Interpreting bitstrings ###

Python properties are used to give different interpretations of the binary data. These properties are calculated only when you ask for them, they're not stored as part of the object.
```
>>> print(h.hex)
000001b3
>>> print(b.oct)
117
>>> print(h.bin)
00000000000000000000000110110011
>>> print(ui.uint)
15
>>> print(ui.bin)  # (note the leading zeros because we gave it a length of 6)
001111 
```

### Manipulating bitstrings ###
You can treat a bitstring just like a list whose elements are all single bits.

Slicing
```
>>> print h[24:32]      # by default indices are in bits
0xb3
>>> print h[3:4:8]      # (the third byte)
0xb3   
>>> print h[-4:]        # (the final four bits)
0b0011 
```
Joining lists
```
>>> bsl = ['0b0', '0b1', BitArray('uint:3=5'), '0xf']
>>> print(BitArray().join(bsl))
0b011011111
```
Appending, prepending, truncating and deleting.
```
>>> s = BitArray('0x00')
>>> s.prepend('0xaa')
>>> s.append('0xbb')
>>> s
BitArray('0xaa00bb')
>>> del s[:4]   # truncate first 4 bits
>>> del s[-4:]  # truncate final 4 bits
>>> s
BitArray('0xa00b')
>>> del s[4:12] # delete 8 bits at bit position 4
>>> s
BitArray('0xab')
```
Using a bitstring as a source for other bitstrings. Here we use a BitStream, which supports a bit position and reading methods:
```
>>> s = BitStream('0x00112233445566778899aabbccddeeff')
>>> print(s.read(1))           
0b0
>>> s.pos += 7            # Move on 7 bits to byte align.
>>> print(s.read(24))       
0x112233
>>> s.find('0x99aa', bytealigned=True)
(72,)
>>> print(s.read(40))      
0x99aabbccdd
```