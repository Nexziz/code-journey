#include <unistd.h>

void ft_putnbr(int nb)
{
    long n;
    long div;
    char c;

    n = nb;
    if (n == 0)
        return ;
    if (n < 0)
    {
        write(1, "-", 1);
        n = -n;
    }
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
