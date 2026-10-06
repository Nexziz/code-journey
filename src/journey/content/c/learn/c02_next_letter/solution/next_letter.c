#include <unistd.h>

int main(void)
{
    char letter;

    letter = 'f';
    letter = letter + 5;
    write(1, &letter, 1);
    write(1, "\n", 1);
    return (0);
}
