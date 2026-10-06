#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>


        int ft_strcmp(char *s1, char *s2);

        int main(int argc, char **argv)
        {
            int r;

            if (argc < 3)
                return (1);
            r = ft_strcmp(argv[1], argv[2]);
            printf("%d\n", (r > 0) - (r < 0));
            return (0);
        }
