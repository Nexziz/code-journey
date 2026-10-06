#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>


        void ft_div_mod(int a, int b, int *div, int *mod);

        int main(int argc, char **argv)
        {
            int div;
            int mod;

            if (argc < 3)
                return (1);
            div = -1;
            mod = -1;
            ft_div_mod(atoi(argv[1]), atoi(argv[2]), &div, &mod);
            printf("%d %d\n", div, mod);
            return (0);
        }
