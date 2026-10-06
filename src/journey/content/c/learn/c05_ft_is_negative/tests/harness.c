#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>


        void ft_is_negative(int n);

        int main(int argc, char **argv)
        {
            if (argc > 1)
                ft_is_negative(atoi(argv[1]));
            write(1, "\n", 1);
            return (0);
        }
