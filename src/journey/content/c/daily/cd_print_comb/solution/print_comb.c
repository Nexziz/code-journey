#include <unistd.h>

static void put_digit(int d)
{
    char c;

    c = '0' + d;
    write(1, &c, 1);
}

int main(void)
{
    int a;
    int b;
    int c;

    a = 0;
    while (a <= 7)
    {
        b = a + 1;
        while (b <= 8)
        {
            c = b + 1;
            while (c <= 9)
            {
                put_digit(a);
                put_digit(b);
                put_digit(c);
                if (!(a == 7 && b == 8 && c == 9))
                    write(1, ", ", 2);
                c++;
            }
            b++;
        }
        a++;
    }
    write(1, "\n", 1);
    return (0);
}
