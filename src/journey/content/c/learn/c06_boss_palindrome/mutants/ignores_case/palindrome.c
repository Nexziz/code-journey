#include <unistd.h>

static char low(char c)
{
    if (c >= 'A' && c <= 'Z')
        return (c + 32);
    return (c);
}

int main(int argc, char **argv)
{
    int i;
    int len;

    if (argc != 2)
    {
        write(1, "\n", 1);
        return (0);
    }
    len = 0;
    while (argv[1][len] != '\0')
        len++;
    i = 0;
    while (i < len / 2)
    {
        if (low(argv[1][i]) != low(argv[1][len - 1 - i]))
        {
            write(1, "no\n", 3);
            return (0);
        }
        i++;
    }
    write(1, "yes\n", 4);
    return (0);
}
