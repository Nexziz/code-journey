#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>


        #include <string.h>

        char *ft_strcpy(char *dest, char *src);

        int main(int argc, char **argv)
        {
            char buf[256];
            char *ret;

            if (argc < 2)
                return (1);
            memset(buf, 'Z', sizeof(buf) - 1);
            buf[255] = '\0';
            ret = ft_strcpy(buf, argv[1]);
            printf("%s|%d\n", buf, ret == buf);
            return (0);
        }
