#include <unistd.h>

int main(void)
{
    write(1, "Ready\n", 6);
    write(1, "Set\n", 4);
    write(1, "Go!\n", 4);
    return (0);
}
