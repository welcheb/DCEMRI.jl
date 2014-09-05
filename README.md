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

Once you have the base Julia install working, you'll need a few packagaes.  These can be 
installed with 

- `Pkg.add("MAT")`
- `Pkg.add("Optim")`
- `Pkg.add("Calculus")`
- `Pkg.add("ArgParse")`

Now you're ready to run the DCE code!

## Running the DCE MRI analysis code.

more text

## QIBA Validation

To perform the validation on the Quantitative Imaging Biomarkers Alliance phantoms for yourself 
from the original DICOMS, you will need to download the DICOMS from [Daniel Barboriak's 
Lab](https://dblab.duhs.duke.edu/modules/QIBAcontent/index.php?id=1).  Then the scripts in the 
`qibav6` and `qibav9` folders will help you translate the DICOM data to MAT files suitable for 
input into the Julia code.

I have already done this step for you and included the MAT files.  This can serve as a quick check that everything is installed correctly.
