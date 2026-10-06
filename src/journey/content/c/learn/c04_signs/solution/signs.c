#include <unistd.h>

int main(void)
{
    int n;

    for (n = -3; n <= 3; n++)
    {
        if (n < 0)
            write(1, "N", 1);
        else if (n == 0)
            write(1, "Z", 1);
        else
            write(1, "P", 1);
    }
    write(1, "\n", 1);
    return (0);
}
