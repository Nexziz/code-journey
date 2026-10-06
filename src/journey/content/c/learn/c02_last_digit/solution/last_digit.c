#include <unistd.h>

int main(void)
{
    int total;
    char digit;

    total = 7 * 8 + 5;
    digit = '0' + total % 10;
    write(1, &digit, 1);
    write(1, "\n", 1);
    return (0);
}
