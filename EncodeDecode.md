N.B. These are ramblings on possible future methods - none of this is implemented yet, so feel free to comment, but don't expect any of this to work!


encode would be much like pack, but would append to the end of current BitString.
```
>>> a = BitString()
>>> a.encode('0x01, 0b1, uint:5=6')
>>> a.encode('0b110')
```
Similarly decode would be like unpack, but would change pos (so just like readlist, but bear with me).
```
>>> a.decode('hex:8, bin:1, uint:5')
'0x01', '0b1', 6
>>> a.decode('bin:3')
'0b110'
```
The fun comes with keywords:
```
>>> a = BitString()
>>> a.encode('0x01=sc, 0b1, uint:5=val', val=6)
>>> a.encode('bin:3=flags', flags='110')
```
After this you have the same bitstring, but can also say
```
>>> a.sc
'0x01'
>>> a.val
6
>>> a.val = 4
```
etc.

So the encode also adds attributes to the BitString for the different fields.

Now let's do the decode:

```
>>> a.decode('0x01=sc, 0b1, uint:5=val')
{'sc': '0x01', 'val': 6}
```

For the literals '0x01' and '0b1' a ParseError will be raised if they are not the values specified in the format string. (Question: Should we even return 'sc' in the dictionary? It can only ever be one value.)
```
>>> a.decode('0b111=flags')
ParseError: flags was '0b110', expected '0b111'.
```

For a BitString created with encode, the decode can be more concise:
```
>>> a.decode('sc, bin:1, val')
{'sc': '0x01', 'val': 6}
```
Note that the unnamed token doesn't get returned. Partly because I can't think of a nice way to do so!

**Format Specifiers**

I'm trying to get to a point where a format can be specified by a string (or many strings) which can then be used both for encoding and decoding. A couple of examples would be helpful:

```
>>> header = '0x000001b3=start_code, uint:12=width, uint:12=height, bin:4=flags'
>>> s = BitString()
>>> s.encode(header, width=352, height=288, flags='1110')
```
Note that naming start\_code isn't strictly neccessary, but I guess it helps in error messages when decoding.
```
>>> s.height //= 2
>>> s.decode(header)
{'width': 352, 'height': 144, 'flags':'0b1110'}
```

Another example:
```
>>> format = '0x47=sync_byte, uint:8=payload_length, bytes:payload_length=payload'
>>> s = BitString()
>>> s.encode(format, payload_length=12, payload=b'123456789abc')
>>> s.decode(format)
{'payload_length': 12, 'payload': b'123456789abc'}
```
We would again get a ParseError if the payload wansn't the expected size.

OK, so a more complete example, from MPEG-2 video.

```
picture_start_code = '0x00000100'
sequence_header_code = '0x000001b3'
...
d = {}
s = Bits(filename='somefile')

def video_sequence():
    next_start_code()
    sequence_header()
    sequence_extension()
    while(True):
        extension_and_user_data(0)
        while(True):
            if nextbits(group_start_code):
                group_of_pictures_header()
            ...
            if nextbits(picture_start_code) or nextbits(group_start_code):
                break
        ...
        if not nextbits(sequence_end_code):
            sequence_header()
            sequence_extension()
        if not nextbits(sequence_end_code):
            break
    s.decode(sequence_end_code)

def sequence_header()
    format = [sequence_header_code,
              'uint:12=horizontal_size_value', 
              'uint:12=vertical_size_value',
              ...
              'True=marker_bit',
              ...
              'bool=load_intra_quantiser_matrix']
    d.update(s.decode(format))
    if d['load_intra_quantiser_matrix']:
        d.update(s.decode('64*uint:8=intra_quantiser_matrix'))
    ...
    next_start_code()

def sequence_extension():
    format = [extension_start_code,
              'uint:4=extension_start_code_identifier',
              'uint:8=profile_and_level_indication',
              'bool=progressive_sequence',
              ...
             ]
    d.update(s.decode(format))
    next_start_code()

              

video_sequence()


```