
all: test static-test

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

static-test:
	mkdir -p static
	cat static-testing | ../objdump-fixup.py > static/testing-od-fixup-output
	cat static-testing | ../objdump-fixup.py -na > static/testing-od-fixup-na-output
	cat static-testing | ../objdump-fixup.py -nm > static/testing-od-fixup-nm-output
	cat static-testing | ../objdump-fixup.py -nam > static/testing-od-fixup-nam-output
	diff static/testing-od-fixup-output static-testing-output
	diff static/testing-od-fixup-na-output static-testing-na-output
	diff static/testing-od-fixup-nm-output static-testing-nm-output
	diff static/testing-od-fixup-nam-output static-testing-nam-output

clean:
	rm -rf testing testing-od-output testing-od-fixup-output testing-od-fixup-na-output testing-od-fixup-nm-output testing-od-fixup-nam-output diffs static *.o *~

