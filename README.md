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
$ objdump -d [file] | objdump-fixup.py | less
````
- 'objdump-fixup.py -na' will remove the leading addresses for each line.
- 'objdump-fixup.py -h' will print the usage.

Tips
----
- c++filt can be added to the pipeline to demangle names
- objdump can take the '--disassemble=' option to specify only a function from the object file to be output.  Note that the name is mangled.
- objdump defaults to AT&T syntax, but -Mintel will output intel syntax
- objdump can intersperse the source with the -S flag
