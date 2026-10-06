#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>


        int ft_max(int a, int b);

        int main(int argc, char **argv)
        {
            if (argc > 2)
                printf("%d\n", ft_max(atoi(argv[1]), atoi(argv[2])));
            return (0);
        }
