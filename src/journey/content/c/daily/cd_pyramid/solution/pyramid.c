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
    int n;
    int row;
    int col;

    if (argc != 2)
        return (0);
    n = parse(argv[1]);
    row = 1;
    while (row <= n)
    {
        col = 0;
        while (col < n - row)
        {
            write(1, " ", 1);
            col++;
        }
        col = 0;
        while (col < 2 * row - 1)
        {
            write(1, "*", 1);
            col++;
        }
        write(1, "\n", 1);
        row++;
    }
    return (0);
}
