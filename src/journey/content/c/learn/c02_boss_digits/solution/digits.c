#include <unistd.h>

int main(void)
{
    int n;
    char c;

    n = 12 * 12 * 12;
    c = '0' + n / 1000;
    write(1, &c, 1);
    c = '0' + n / 100 % 10;
    write(1, &c, 1);
    c = '0' + n / 10 % 10;
    write(1, &c, 1);
    c = '0' + n % 10;
    write(1, &c, 1);
    write(1, "\n", 1);
    return (0);
}
