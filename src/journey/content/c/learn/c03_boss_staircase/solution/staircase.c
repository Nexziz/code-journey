#include <unistd.h>

int main(void)
{
    int row;
    int col;
    char c;

    for (row = 1; row <= 5; row++)
    {
        for (col = 0; col < row; col++)
        {
            c = 'a' + col;
            write(1, &c, 1);
        }
        write(1, "\n", 1);
    }
    return (0);
}
