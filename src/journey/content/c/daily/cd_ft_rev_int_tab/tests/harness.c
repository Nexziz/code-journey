#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>


    void ft_rev_int_tab(int *tab, int size);

    int main(int argc, char **argv)
    {
        int n;
        int i;
        int *tab;

        n = argc - 1;
        tab = malloc(sizeof(int) * (n > 0 ? n : 1));
        i = 0;
        while (i < n)
        {
            tab[i] = atoi(argv[i + 1]);
            i++;
        }
        ft_rev_int_tab(tab, n);
        i = 0;
        while (i < n)
        {
            printf(i ? " %d" : "%d", tab[i]);
            i++;
        }
        printf("\n");
        free(tab);
        return (0);
    }
