#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>


        int ft_is_prime(int nb);

        int main(int argc, char **argv)
        {
            if (argc > 1)
                printf("%d\n", ft_is_prime(atoi(argv[1])));
            return (0);
        }
