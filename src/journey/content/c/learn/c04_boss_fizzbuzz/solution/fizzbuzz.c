#include <unistd.h>

int main(void)
{
    int i;
    char c;

    for (i = 1; i <= 15; i++)
    {
        if (i % 15 == 0)
            write(1, "FizzBuzz", 8);
        else if (i % 3 == 0)
            write(1, "Fizz", 4);
        else if (i % 5 == 0)
            write(1, "Buzz", 4);
        else
        {
            if (i >= 10)
            {
                c = '0' + i / 10;
                write(1, &c, 1);
            }
            c = '0' + i % 10;
            write(1, &c, 1);
        }
        write(1, "\n", 1);
    }
    return (0);
}
