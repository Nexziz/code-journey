#include <unistd.h>

void ft_putnbr(int nb)
{
    int div;
    char c;

    if (nb < 0)
    {
        write(1, "-", 1);
        nb = -nb;
    }
    div = 1;
    while (nb / div >= 10)
        div *= 10;
    while (div > 0)
    {
        c = '0' + nb / div % 10;
        write(1, &c, 1);
        div /= 10;
    }
}
