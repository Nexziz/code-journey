#include <unistd.h>

int main(void)
{
    char c;
    char out;

    for (c = 'a'; c <= 'z'; c++)
    {
        out = c;
        if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u')
            out = c - 'a' + 'A';
        write(1, &out, 1);
    }
    write(1, "\n", 1);
    return (0);
}
