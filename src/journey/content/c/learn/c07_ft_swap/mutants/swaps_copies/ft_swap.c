void ft_swap(int *a, int *b)
{
    int x;
    int y;
    int tmp;

    x = *a;
    y = *b;
    tmp = x;
    x = y;
    y = tmp;
    (void)x;
    (void)y;
}
