#include <unistd.h>

int main(void)
{
    int a;
    int b;
    int c;
    char out[3];

    a = 0;
    while (a <= 7)
    {
        b = a + 1;
        while (b <= 8)
        {
            c = b + 1;
            while (c <= 9)
            {
                out[0] = '0' + a;
                out[1] = '0' + b;
                out[2] = '0' + c;
                write(1, out, 3);
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
