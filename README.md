# code-journey

Practise C and Python in your terminal. Pick a task, write it in your own editor, hand it in
with git. It is graded the moment you push.

## Start

You need Python 3.11+, git, and `gcc` or `clang` if you want C.

```sh
git clone https://github.com/Nexziz/code-journey && cd code-journey
pip install -e .
journey
```

The first time it asks C or Python. After that `journey` shows a short menu:

```
  1  Continue   Hello, terminal
  2  Daily      Pascal's pyramid        new
  3  Weekly     unlocks at level 5
  4  Versus     coming soon
```

Pick a number. You get the question and a folder to work in.

## Hand it in

```sh
journey check                                    # test it first, nothing is recorded
git add . && git commit -m "done" && git push    # graded right away
```

A passing push moves you on. Daily and weekly tasks also change your rating, depending on how fast
and how cleanly you solve them.

## More

- Switch language: `journey track python` or `journey track c`.
- Write your own tasks: [docs/AUTHORING.md](docs/AUTHORING.md).
- How it works and where it is going: [docs/DESIGN.md](docs/DESIGN.md).

## Good to know

- Your code runs on your own machine, with time limits and (for C) memory checks. It is not a
  security sandbox, and the hidden tests are readable on your disk. It is you against the clock.
- Linux, macOS and WSL work. Native Windows is untested.

## Development

```sh
pip install -e . ruff
ruff check src tests && ruff format --check src tests
python -m unittest discover -s tests -t .
```
