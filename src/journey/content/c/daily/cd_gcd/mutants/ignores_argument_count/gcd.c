#include <unistd.h>

static int parse(char *s)
{
    int i;
    int n;

    i = 0;
    n = 0;
    while (s[i] >= '0' && s[i] <= '9')
    {
        n = n * 10 + (s[i] - '0');
        i++;
    }
    return (n);
}

int main(int argc, char **argv)
{
    int a;
    int b;
    int tmp;
    char c;

    (void)argc;
    a = parse(argv[1]);
    b = parse(argv[2]);
    while (b != 0)
    {
        tmp = b;
        b = a % b;
        a = tmp;
    }
    c = '0' + a % 10;
    write(1, &c, 1);
    write(1, "\n", 1);
    return (0);
}
