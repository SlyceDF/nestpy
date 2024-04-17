## nestPython


*"what if python, with braces, one line?"*

# SETUP

Install nestPython by executing:
```bash
$ pip install nestpython
```
After importing;

- In order to compile a string from nestPython to python, use `nestpython.ncompile(string)`
- In order to execute a nestPython string, use `nestpython.nexec(string)`

	For both, optional argument `indent-level` determines the indentation increment in the resulting python file. It is set to 1 by default.
-  To execute and compile files and folders, use the `nestpython.files` module:
	-  `nestpython.files.ncompile(file)`  compiles the given file to a string
	-  `nestpython.files.nexec(file)` executes the file
    -  `nestpython.files.build(dir, new_dir)` builds an entire golder
    -  arguments can be provided.

Use `.npy` for nestPython files, `.npx` for nestCython files.

# FEATURING:
## braces

Use `{`, `;` and `}` instead of indentation! Indentation and newlines in the source files will be ignored. e.g.:

```nestpython
n = input('Enter Number: ');
if (n % 2 == 0) {
	print('n is even')
} else {
	print('n is odd')
}
```

Use `~{` as a shorthand for `while True {`. 

## syntactical changes

Several keywords are altered:

|  Python  | nestPython |  Python  | nestPython |
|:--------:|:----------:|:--------:|:----------:|
|  `def`   |    `:=`    |  `del`   |    `~>`    |
| `return` |    `=>`    |  `and`   |    `&&`    |
|   `in`   |    `->`    |   `or`   |   `\|\|`   |
| `not in` |    `!>`    |   `:=`   |    `<-`    |
|   `is`   |    `=&`    | `assert` |    `?!`    |
| `is not` |   `!=&`    |  `case`  |    `?`     |
| `lambda` |    `;=`    |   `;`    |    `,,`    |
|   `->`   |    `>:`    |   `//`   |    `~/`    |
|  `+= 1`  |    `++`    |  `-= 1`  |    `--`    |
|   `{`    |    `-{`    |   `}`    |    `}-`    |


A variable like `return` will be replaced with `return_` on transpilation. `pass` is not required: simply use `{}`. 
Note that one-liner functions can still be written with colons: `:= foo(): => bar`

Cython keywords are also altered for `.npx`:

| Cython  | nestCython |
|:-------:|:----------:|
| `cdef`  |    `$=`    |
| `cpdef` |   `~$=`    |

## comments

- For block comments, use `/*`, `*/`.
- For line comments, use `//`.
- Block and line comments will be ignored during compilation.
- For comments that need to be transpiled into python ones, use `/|`, `|\ `.

*(to be continued)*

---
github : https://github.com/slycedf/nestpy 
  
pypi : https://pypi.org/project/nestpython
