#include <unistd.h>

static void put_number(int n)
{
    int div;
    char c;

    div = 1;
    while (n / div >= 10)
        div *= 10;
    while (div > 0)
    {
        c = '0' + n / div % 10;
        write(1, &c, 1);
        div /= 10;
    }
}

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

    if (argc != 3)
    {
        write(1, "\n", 1);
        return (0);
    }
    a = parse(argv[1]);
    b = parse(argv[2]);
    while (b != 0)
    {
        tmp = b;
        b = a % b;
        a = tmp;
    }
    put_number(a);
    write(1, "\n", 1);
    return (0);
}
