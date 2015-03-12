Note: This was implemented in version 2.1.

# Introduction #

The Bits / BitString classes could be considered to be too complex. In particular the 'stream' facilities (i.e. those methods which use the bit position) are often unneeded. When comparing objects the position isn't used, which complicates things. And of course it increases the memory footprint of every instance.

Suggest a reorganisation of classes to introduce classes without bit positions.


---


New basic types:

  * `Bits` : Immutable bits. No bit position
  * `BitArray` : Mutable bits. No bit position
  * `ConstBitStream` : Immutable bitstream.
  * `BitStream` : Mutable bitstream.

The hierarchy is:

```
        Bits
       /    \
      /      \
     /        \
 BitArray  ConstBitStream
     \        /
      \      /
       \    /
      BitStream
```

so `BitArray` adds mutating methods to `Bits`, `ConstBitStream` adds reading and bit positions to `Bits`, while `BitStream` just inherits from them both and doesn't really add anything.

So the current `Bits` becomes `ConstBitStream` (or a better name if I can think of one), and `BitString` becomes `BitStream`. And so we lose the `BitString` class altogether.

The `BitArray` name is probably the best choice. It then matches the in-built `bytes` and `bytearray` types. There is a bit of a clash with the bitarray module, but their class is `bitarray.bitarray` and mine is `bitstring.BitArray` so it's not too bad.

Some other random thoughts:

  * The `BitString` name could be left as an alias to `BitStream` to aid backward compatibility.
  * This can't be done in 2.x because of the renaming of `Bits`. Or alternatively we could call it `ConstBitArray` for 2.x and consider renaming it later? In that case we leave `Bits` in as an alias for `ConstBitStream` instead.
  * I'd like to get to a stage where it would be possible to open a file for writing and have it contain the mutable bit data. This would probably have to be a 3.x feature or have a clunky 2.x interface.


---


Another possible naming is:
```
        Bits
       /    \
      /      \
     /        \
 BitArray  BitStream
     \        /
      \      /
       \    /
      BitString
```