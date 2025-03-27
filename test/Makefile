
all: test


test: testing
	objdump -d testing > testing-od-output
	objdump -d testing | ../objdump-fixup.py > testing-od-fixup-output
	objdump -d testing | ../objdump-fixup.py -na > testing-od-fixup-na-output
	objdump -d testing | ../objdump-fixup.py -nm > testing-od-fixup-nm-output
	objdump -d testing | ../objdump-fixup.py -nam > testing-od-fixup-nam-output
	diff testing-od-output testing-od-fixup-output > diffs || exit 0
	wc -l testing-od-output
	wc -l testing-od-fixup-output
	wc -l testing-od-fixup-na-output
	wc -l testing-od-fixup-nm-output
	wc -l testing-od-fixup-nam-output

clean:
	rm -rf testing testing-od-output testing-od-fixup-output testing-od-fixup-na-output testing-od-fixup-nm-output testing-od-fixup-nam-output diffs *.o *~

