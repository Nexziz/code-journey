#include <unistd.h>

int main(void)
{
    int i;
    char c;

    for (i = 0; i < 10; i += 2)
    {
        c = '0' + i;
        write(1, &c, 1);
    }
    write(1, "\n", 1);
    return (0);
}
