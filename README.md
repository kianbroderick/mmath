# mmath
A mental math training TUI application. Built with Python using the `textual` library.

## Features
- Many operations, including arithmetic, exponents, fractions, complex numbers, unit conversions, and day of the week questions.
- Supports quizzes with an arbitrary number of questions and maximum number limit.
- Options to set a limit on the time per question and make the question vanish after a time.
- Detailed data screen

## Usage
Run `mmath` from the command line to start the application. Press `h` to view the help screen which details the options.

# Installation
With `uv`, run 
```
git clone https://github.com/kianbroderick/mmath_tui.git
cd mmath_tui
uv sync
uv run mmath
```
to clone and run the program.

# Future improvements
- add a screen to type in memorized digits of pi or e
- more operations
- add score tracking and statistics over multiple runs

## License
`mmath` is liscense under the terms of the MIT License.
