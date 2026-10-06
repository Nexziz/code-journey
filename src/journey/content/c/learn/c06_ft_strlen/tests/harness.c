#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>


        int ft_strlen(char *str);

        int main(int argc, char **argv)
        {
            if (argc > 1)
                printf("%d\n", ft_strlen(argv[1]));
            return (0);
        }
