DCEMRI.jl
=========

Julia language tools for the analysis of dynamic contrast enhanced magnetic resonance imaging
(DCE MRI) data.

## Why Julia?

From the [Julia website](http://julialang.org/),

> Julia is a high-level, high-performance dynamic programming language for technical computing, with syntax that is familiar to users of other technical computing environments. It provides a sophisticated compiler, distributed parallel execution, numerical accuracy, and an extensive mathematical function library. The library, largely written in Julia itself, also integrates mature, best-of-breed C and Fortran libraries for linear algebra, random number generation, signal processing, and string processing. *

Basically, it looks like Matlab, which is simple to learn and familiar to most MRI researchers, but it works better and faster and is completely free.  In particular, for the problem of DCE MRI, Julia's simple and flexible parallel computing model allows almost perfect parallelization of the nonlinear least squares fitting problem.  In my informal testing, the basic speed of Julia coupled to my parallel implementation produced a factor of 20-40 speedup over comparable Matlab and Python.

## Julia Installation

I've tried to keep the software dependencies to a minimum.  So to run this code you must install only the Julia programming language.  Julia can be downloaded from [julialang.org](http://julialang.org/downloads/) as pre-compiled binaries or cloned from the [github repository](https://github.com/JuliaLang/julia).  If you clone the Julia github repo, you should be able to make it with a simple `make` command in the top-level source directory.  The compilation might take a while, but it is fairly automatic.

Once you have the base Julia install working, go ahead and start it up.  You might need to set
your PATH shell variable to point to your install location, or you may just be able to click on
the icon if you installed one of the pre-compiled binaries.

Next you'll need a few Julia packagaes.  These can be installed at the Julia prompt with

- `julia> Pkg.add("MAT")`
- `julia> Pkg.add("Optim")`
- `julia> Pkg.add("Calculus")`
- `julia> Pkg.add("ArgParse")`

Now you're ready to run the DCE code!

## A Note about Units

All units in the code are SI where possible.  Sometimes, due to numerical accuracy issues, they have been converted internally. But all data should be supplied to the code in SI units.  In particular, time should be in seconds, and relaxation rates in inverse seconds.  Flip angles should be in degrees.

## Running the Code

DCEMRI.jl has two basic modes of operation.  The first is command-line invocation, as you would with an operating system command.  To run DCEMRI.jl as a command, first edit the first `process_dcemri.jl` of the text file to point to your Julia binary, as in
```
#!/path/to/julia/binary
```
Next, make sure the `process_dcemri.jl` file is executable.  It should already be.

The script run as a command can parse arguments passed on the command line to configure the model and point to the input data and output file.  To see the available options, run `./process_dcemri.jl -h` at the terminal prompt, you will get
```
usage: process_dcemri_data.jl [-O OUTFILE] [-R RELAXIVITY] [-r TR]
                        [-d DCEFLIP] [-t T1FLIP [T1FLIP...]] [-x] [-p]
                        [-w WORKERS] [-v] [-h] [datafile]

Process DCE-MRI data. Optional arguments can be used to override any
values found in input files. For questions, contact David Smith
<david.smith@gmail.com>. For bug reports and feature requests, file an
issue at http://github.com/davidssmith/DCEMRI.jl

positional arguments:
  datafile              path to MAT file containing DCE and T1 data
                        (default: "invivo.mat")

optional arguments:
  -O, --outfile OUTFILE
                        path to MAT file to contain the ouput
                        (default: "dceout.mat")
  -R, --relaxivity RELAXIVITY
                        contrast agent relaxivity (1/s) (type:
                        Float64)
  -r, --TR TR           repetition time (ms) (type: Float64)
  -d, --dceflip DCEFLIP
                        flip angle of DCE data (type: Float64)
  -t, --t1flip T1FLIP [T1FLIP...]
                        flip angle(s) of T1 data (type: Float64)
  -x, --extended        use Extended Tofts-Kety instead of Standard
  -p, --plotting        plot intermediate results
  -w, --workers WORKERS
                        number of parallel workers to use (one per CPU
                        core is best) (type: Int64, default: 4)
  -v, --verbose         show verbose output
  -h, --help            show this help message and exit


```

To process a DCEMRI data set from the command line, the minimum invocation is
`./process_dcemri.jl /path/to/my/dce/data.mat`.

The input data MAT file must contain the following:
- `aif`: Arterial input function (Cp) as a vector, resampled to the DCE time points.
- `dcedata`: DCE data as a 3-D array (1 time by 2 space dimensions).
- `t`: time vector representing the dcedata samples.
- T1 information as either `R1map` and `S0map`, representing pre-calculated R1 relaxation maps, or as `t1data`, indicating that
a multi-flip scan was performed and must be analyzed.  If `t1data` is supplied, the code also needs `t1flip`, a vector of flip angles for the multi-flip data.


## Running the In Vivo Demo

If you are not already in the DCEMRI.jl source directory, you can navigate there from within
the Julia environment by pressing `;` to obtain the `shell>` prompt and then navigating there
with shell commands.  After each shell command, you will need to press `;` again to drop back into the `shell>` prompt.  The semicolon acts as
a shell command prefix.  The fancy prompt change acts as a reminder that the next text you enter will be interpreted by the shell.

Once you are in the DCEMRI.jl directory, you can run the in vivo data demo with the command
`include("demo_invivo.jl")`.  After a few seconds to a few minutes, depending on the speed of your machine, you will see the following output text:

```
julia> include("demo_invivo.jl")
importing modules
starting workers
reading input data
found multi-flip data
fitting R1 relaxation rate to multi-flip data
fitting 6109 x 10 points on each of 3 workers
computing signal enhancement ratios
converting signal S to effective R1 relaxation rate
converting effective R1 to tracer tissue concentration Ct
fitting Standard Tofts-Kety model to tissue concentration Ct
fitting 4337 x 25 points on each of 3 workers
saving results to dceout.mat
```

## Running the QIBA Validation

To perform the validation on the Quantitative Imaging Biomarkers Alliance phantoms for yourself
from the original DICOMS, you will need to download the DICOMS from [Daniel Barboriak's
Lab](https://dblab.duhs.duke.edu/modules/QIBAcontent/index.php?id=1).  Then the scripts in the
`qibav6` and `qibav9` folders will help you translate the DICOM data to MAT files suitable for
input into the Julia code.

I have already done this step for you and included the MAT files.  This can serve as a quick check that everything is installed correctly.

