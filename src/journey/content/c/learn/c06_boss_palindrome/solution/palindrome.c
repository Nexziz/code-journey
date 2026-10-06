#include <unistd.h>

static int str_len(char *s)
{
    int i;

    i = 0;
    while (s[i] != '\0')
        i++;
    return (i);
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
    len = str_len(argv[1]);
    i = 0;
    while (i < len / 2)
    {
        if (argv[1][i] != argv[1][len - 1 - i])
        {
            write(1, "no\n", 3);
            return (0);
        }
        i++;
    }
    write(1, "yes\n", 4);
    return (0);
}
