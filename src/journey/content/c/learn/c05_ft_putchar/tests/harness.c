#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>


        void ft_putchar(char c);

        int main(int argc, char **argv)
        {
            if (argc > 1)
                ft_putchar(argv[1][0]);
            return (0);
        }
