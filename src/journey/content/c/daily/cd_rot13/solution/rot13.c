#include <unistd.h>

static char rot13(char c)
{
    if (c >= 'a' && c <= 'z')
        return ((c - 'a' + 13) % 26 + 'a');
    if (c >= 'A' && c <= 'Z')
        return ((c - 'A' + 13) % 26 + 'A');
    return (c);
}

int main(int argc, char **argv)
{
    int i;
    char c;

    if (argc == 2)
    {
        i = 0;
        while (argv[1][i] != '\0')
        {
            c = rot13(argv[1][i]);
            write(1, &c, 1);
            i++;
        }
    }
    write(1, "\n", 1);
    return (0);
}
