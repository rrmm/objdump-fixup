# objdump-fixup

objdump-fixup assigns locally scoped labels to the output of
objdump(1).  It can be used with Intel or AT&T assembly syntax.

For example, objdump might output:
````
  4046db:       eb 1a                   jmp    4046f7 <main+0x12f>
````
which will be transformed into

````
  4046db:       eb 1a                   jmp    .L0005 <main+0x12f> 4046f7
````
The computed target address and offset is retained for reference. And
the local label is inserted before the appropriate address:
````
.L0005:
  4046f7:       48 83 c4 38             add    $0x38,%rsp
````
Usage
-----
````
Usage:
	objdump-fixup.py [options]

Options:
	-na		   do not display the address
	-nm		   do not display the machine code
	-nam		  do not display the address or the machine code
	-h, --help	display this help and exit

Filters the output from objdump to add local labels to the disassembly.

    $ objdump -d [execfile] | objdump-fixup.py

````
Tips
----
- c++filt can be added to the pipeline to demangle names
- objdump can take the '--disassemble=' option to specify only a function from the object file to be output.  Note that the name is mangled.
- objdump defaults to AT&T syntax, but -Mintel will output intel syntax
- objdump can intersperse the source with the -S flag
