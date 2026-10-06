int ft_atoi(char *str)
{
    int i;
    int neg;
    int result;

    i = 0;
    while (str[i] == ' ')
        i++;
    neg = 0;
    if (str[i] == '-' || str[i] == '+')
    {
        neg = (str[i] == '-');
        i++;
    }
    result = 0;
    while (str[i] >= '0' && str[i] <= '9')
    {
        result = result * 10 - (str[i] - '0');
        i++;
    }
    if (neg)
        return (result);
    return (-result);
}
