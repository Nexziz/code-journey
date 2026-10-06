#include <unistd.h>

static void put_number(long n)
{
    long div;
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

static int is_space(char c)
{
    return (c == ' ' || (c >= 9 && c <= 13));
}

int main(void)
{
    char buf[4096];
    long got;
    long i;
    long lines;
    long words;
    long chars;
    int in_word;

    lines = 0;
    words = 0;
    chars = 0;
    in_word = 0;
    got = read(0, buf, sizeof(buf));
    while (got > 0)
    {
        i = 0;
        while (i < got)
        {
            chars++;
            if (buf[i] == '\n')
                lines++;
            if (is_space(buf[i]))
                in_word = 0;
            else if (!in_word)
            {
                in_word = 1;
                words++;
            }
            i++;
        }
        got = read(0, buf, sizeof(buf));
    }
    put_number(lines);
    write(1, " ", 1);
    put_number(words);
    write(1, " ", 1);
    put_number(chars);
    write(1, "\n", 1);
    return (0);
}
