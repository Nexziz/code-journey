#include <unistd.h>

int main(int argc, char **argv)
{
    int i;
    int count;
    char c;

    count = 0;
    if (argc == 2)
    {
        i = 0;
        while (argv[1][i] != '\0')
        {
            c = argv[1][i];
            if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u'
                || c == 'A' || c == 'E' || c == 'I' || c == 'O' || c == 'U')
                count++;
            i++;
        }
    }
    c = '0' + count;
    write(1, &c, 1);
    write(1, "\n", 1);
    return (0);
}
