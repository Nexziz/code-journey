#include <unistd.h>

int main(void)
{
    write(1, "+---------+\n", 12);
    write(1, "| journey |\n", 12);
    write(1, "+---------+\n", 12);
    return (0);
}
