DCEMRI.jl
=========

Julia language tools for the analysis of dynamic contrast enhanced magnetic resonance imaging
(DCE MRI) data

## Julia Installation

To run this code you must install at the bare minimum the Julia programming language.  This can
be downloaded from [julialang.org](http://julialang.org/downloads/) as pre-compiled binaries or
cloned from the [github repository](https://github.com/JuliaLang/julia).  If you clone the
Julia github repo, you should be able to make it with a simple `make` command in the top-level
source directory.  The compilation might take a while, but it is fairly automatic.

Once you have the base Julia install working, go ahead and start it up.  You might need to set
your PATH shell variable to point to your install location, or you may just be able to click on
the icon if you installed one of the pre-compiled binaries.

Next you'll need a few packagaes.  These can be installed at the Julia prompt with

- `julia> Pkg.add("MAT")`
- `julia> Pkg.add("Optim")`
- `julia> Pkg.add("Calculus")`
- `julia> Pkg.add("ArgParse")`

Now you're ready to run the DCE code!

## Running the In Vivo Demo.

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

## QIBA Validation

To perform the validation on the Quantitative Imaging Biomarkers Alliance phantoms for yourself
from the original DICOMS, you will need to download the DICOMS from [Daniel Barboriak's
Lab](https://dblab.duhs.duke.edu/modules/QIBAcontent/index.php?id=1).  Then the scripts in the
`qibav6` and `qibav9` folders will help you translate the DICOM data to MAT files suitable for
input into the Julia code.

I have already done this step for you and included the MAT files.  This can serve as a quick check that everything is installed correctly.

## Running the Code on Your Data

The other way to run DCEMRI.jl is from the command shell directly, without starting Julia at all.  The script can parse arguments passed in on the command line to configure the model and point to the input data and output file.

If you run `./process_dcemri.jl -h` at the terminal prompt, you will get
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
