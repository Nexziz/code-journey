#include <unistd.h>

static int skip_forward(char *code, int pc)
{
    int depth;

    depth = 1;
    while (depth > 0)
    {
        pc++;
        if (code[pc] == '[')
            depth++;
        else if (code[pc] == ']')
            depth--;
    }
    return (pc);
}

static int skip_back(char *code, int pc)
{
    int depth;

    depth = 1;
    while (depth > 0)
    {
        pc--;
        if (code[pc] == ']')
            depth++;
        else if (code[pc] == '[')
            depth--;
    }
    return (pc);
}

int main(int argc, char **argv)
{
    unsigned char tape[2048];
    char *code;
    int ptr;
    int pc;
    int i;

    if (argc != 2)
    {
        write(1, "\n", 1);
        return (0);
    }
    code = argv[1];
    i = 0;
    while (i < 2048)
    {
        tape[i] = 0;
        i++;
    }
    ptr = 0;
    pc = 0;
    while (code[pc] != '\0')
    {
        if (code[pc] == '>')
            ptr++;
        else if (code[pc] == '<')
            ptr--;
        else if (code[pc] == '+')
            tape[ptr]++;
        else if (code[pc] == '-')
            tape[ptr]--;
        else if (code[pc] == '.')
            write(1, &tape[ptr], 1);
        else if (code[pc] == '[' && tape[ptr] == 0)
            pc = skip_forward(code, pc);
        else if (code[pc] == ']' && tape[ptr] != 0)
            pc = skip_back(code, pc);
        pc++;
    }
    return (0);
}
