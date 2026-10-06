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

int main(void)
{
    char buf[1024];
    long got;
    long i;
    long lines;
    long words;
    int in_word;

    lines = 0;
    words = 0;
    in_word = 0;
    got = read(0, buf, sizeof(buf));
    i = 0;
    while (i < got)
    {
        if (buf[i] == '\n')
            lines++;
        if (buf[i] == ' ' || buf[i] == '\n')
            in_word = 0;
        else if (!in_word)
        {
            in_word = 1;
            words++;
        }
        i++;
    }
    put_number(lines);
    write(1, " ", 1);
    put_number(words);
    write(1, " ", 1);
    put_number(got < 0 ? 0 : got);
    write(1, "\n", 1);
    return (0);
}
