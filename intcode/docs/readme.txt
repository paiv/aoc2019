Intcode
==

Intcode machine from AoC 2019 days 2, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25.


VM
--
$ intcode r -h
usage: intcode run [-h] [-r DRIVER] [-a] infile

positional arguments:
  infile                Input assembly

optional arguments:
  -h, --help            show this help message and exit
  -r DRIVER, --driver DRIVER
                        Driver class, module:name
  -a, --ascii           ASCII I/O


Disassembler
--

$ intcode d -h
usage: intcode disassemble [-h] [-o OUTFILE] [infile]

positional arguments:
  infile                Input assembly

optional arguments:
  -h, --help            show this help message and exit
  -o OUTFILE, --outfile OUTFILE
                        Write output to file


Debugger
--

$ intcode ida -h
usage: intcode debugger [-h] [-r DRIVER] infile

positional arguments:
  infile                Input assembly

optional arguments:
  -h, --help            show this help message and exit
  -r DRIVER, --driver DRIVER
                        Driver class, module:name


Assembler
--

TBD
