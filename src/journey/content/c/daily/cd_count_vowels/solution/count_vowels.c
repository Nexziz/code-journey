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

static int is_vowel(char c)
{
    return (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u'
        || c == 'A' || c == 'E' || c == 'I' || c == 'O' || c == 'U');
}

int main(int argc, char **argv)
{
    int i;
    int count;

    count = 0;
    if (argc == 2)
    {
        i = 0;
        while (argv[1][i] != '\0')
        {
            if (is_vowel(argv[1][i]))
                count++;
            i++;
        }
    }
    put_number(count);
    write(1, "\n", 1);
    return (0);
}
