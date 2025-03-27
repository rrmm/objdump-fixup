#include <stdio.h>

int
fib(int n)
{
    if (n < 2) {
        return 1;
    } else {
        return n*fib(n-1);
    }
}

void
func_A()
{
    int n = 5;
    printf("func_A: fib(%i) = %i\n", n, fib(n));
}

int
main(int argc, char ** argv)
{
    int i;

    func_A();

    printf("hello world\n");

    for (i = 0; i < argc; i++) {
        printf("%s\n", argv[i]);
    }

    return 0;
}
