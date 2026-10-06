#include <unistd.h>

int main(void)
{
    int n;
    char c;

    for (n = 1; n <= 9; n++)
    {
        if (n % 3 == 0)
            write(1, "*", 1);
        else
        {
            c = '0' + n;
            write(1, &c, 1);
        }
    }
    write(1, "\n", 1);
    return (0);
}
