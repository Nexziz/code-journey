#include <unistd.h>

int main(int argc, char **argv)
{
    int i;
    int len;

    (void)argc;
    len = 0;
    while (argv[1][len] != '\0')
        len++;
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
