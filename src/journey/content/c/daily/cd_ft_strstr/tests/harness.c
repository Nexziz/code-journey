#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>


        char *ft_strstr(char *str, char *to_find);

        int main(int argc, char **argv)
        {
            char *found;

            if (argc < 3)
                return (1);
            found = ft_strstr(argv[1], argv[2]);
            if (found)
                printf("%d\n", (int)(found - argv[1]));
            else
                printf("-1\n");
            return (0);
        }
