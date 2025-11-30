# mmath
A mental math training TUI application. Built with Python using the `textual` library.

## Features
- Covers many of the standard mental math challenges, including arithmetic, exponents, fractions, complex numbers, unit conversions, and day of the week questions.
- Supports quizzes with an arbitrary maximum number limit and number of questions.
- Options to set a limit on the time per question and make the question vanish after a specified period.
- Detailed data screen with options to question type, question time, or number of mistakes

## Guides
There are many resources available that detail methods to calculate quickly and accurately.
- <a href="https://worldmentalcalculation.com/advanced-calculation-methods/">World Mental Calculation</a>
- <a href="https://a.co/d/gnyceGX">Secrets of Mental Math,</a> by Arthur Benjamin and Michael Shermer

## Gallery
| ![Main Menu](./img/main_menu.png)  | ![Question Screen](./img/question.png)  |
|------------------------------------|----------------------------------------|
| ![End Screen](./img/end_screen.png)| ![Data Screen](./img/data_screen.png)  |

## Usage
Run `mmath` from the command line to start the application. Press `h` to view the help screen which details the options.

# Installation
### 1. With <a href="https://docs.astral.sh/uv/">`uv`</a>
`mmath` can be run with <a href="https://docs.astral.sh/uv/">`uv`</a> with the command
```
uvx mentalmath
```
It can be installed with
```
uv tool install mentalmath
```
and then run with `mmath` from the command line.

To build from source with <a href="https://docs.astral.sh/uv/">`uv`</a>, run
```
git clone https://github.com/kianbroderick/mmath.git
cd mmath
uv pip install -e .
```
to clone the repository and install the program to a virtual environment.

### 2. Using `pip`
`mmath` can be installed with pip with the following commands:
```
git clone https://github.com/kianbroderick/mmath.git
cd mmath
```
Install `textual` in either the global or virtual evironment with
```
pip install textual
```
Run the application with
```
pip install -e .
mmath
```
# Future improvements
- add a screen to type in memorized digits of pi or e
- more operations
- add score tracking and statistics over multiple sessions

## License
`mmath` is licensed under the terms of the MIT License.
