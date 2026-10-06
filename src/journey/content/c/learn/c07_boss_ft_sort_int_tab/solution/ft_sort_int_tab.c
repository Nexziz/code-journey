void ft_sort_int_tab(int *tab, int size)
{
    int i;
    int tmp;
    int swapped;

    swapped = 1;
    while (swapped)
    {
        swapped = 0;
        i = 0;
        while (i + 1 < size)
        {
            if (tab[i] > tab[i + 1])
            {
                tmp = tab[i];
                tab[i] = tab[i + 1];
                tab[i + 1] = tmp;
                swapped = 1;
            }
            i++;
        }
    }
}
