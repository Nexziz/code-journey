code = "for r in range(10):\n"
code = code + "    s = ' ' * (2 * (9 - r))\n"
code = code + "    v = 1\n"
code = code + "    for k in range(r + 1):\n"
code = code + "        s = s + str(v).rjust(4)\n"
code = code + "        v = v * (r - k) // (k + 1)\n"
code = code + "    print(s)\n"
exec(code)
