# Arduino-ATMEGA328-binary-reversing

Steps:
1. Extract binary file from Atmega328 chip or obtain .hex file from buildfolder
      * If .hex file convert to bin with [online tool](http://matrixstorm.com/avr/hextobin/ihexconverter.html?ref=blog.attify.com)
2. IDA doesn't know the memory map of ATMEGA328, overwrite avr.cfg to the cfg folder of IDA (ATMEGA328 is appended to the file)
3. Load the binary in IDA, choose AVR processor. Select ATMEGA328.
4. File -> Script File -> [diaphora.py](https://github.com/joxeankoret/diaphora), compare against a build of with symbols intact (.elf) file.
5. Extract initialised RAM from BINfile. Use > ram_extractor.py
6. Add RAM segment to IDA.

Credits to (they explain things in more detail):

[Barun](https://blog.attify.com/flare-4-ctf-write-part-4/)

[Thanatos](http://thanat0s.trollprod.org/2014/01/loader-un-binaire-arduino-dans-ida/?ref=blog.attify.com)
