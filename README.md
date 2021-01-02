# About

This repository contains the TeX source code for the specification documents of the programming language named [“Zilch”](https://github.com/zilch-lang).

# Compiling

To install `latexmk` (which is used to compile the PDF file), you will need to follow the instructions given [here](https://mg.readthedocs.io/latexmk.html).
On Linux and Mac, you will also need `texlive`. On Windows, you will need `MikTeX`.

Once done, you will also need [GNU make](https://www.gnu.org/software/make/) (it should already be installed on Linux and Mac environments).

> **NOTE:** on NixOS or any other nix-running system, you only need to start a new nix-shell, and everything will be installed and ready to use.

To compile the PDF file, you just need to type `make` in a terminal, and the PDF file will come as `magical-zilch-book.pdf` in the root folder of the cloned repository.

# Contributing

Everybody makes typing mistakes.
Because I'm not English (my main language is French), I may also make grammar mistakes.
If you spot any, don't hesitate to either open an issue or a pull request, correcting it!

# License and copyright

This repository is licensed under the BSD-3 license found in the [LICENSE](./LICENSE) file.
