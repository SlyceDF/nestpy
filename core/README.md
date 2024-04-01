## nestpy


*"what if python, with braces, one line?"*

# SETUP

Install nestpy by executing:
```bash
$ pip install nestpython
```
After importing;

- In order to compile a string from nestpy to python, use `nestpy.ncompile(string)`
- In order to execute a nestpy string, use `nestpy.nexec(string)`

	For both, optional argument `indent-level` determines the indentation increment in the resulting python file. It is set to 1 by default.
-  To execute and compile files and folders, use the `nestpy.files` module:
	-  `nestpy.files.ncompile(file)`  compiles the given file to a string
	-  `nestpy.files.nexec(file)` executes the file
    -  `nestpy.files.build(dir, new_dir)` builds an entire golder
    -  arguments can be provided.

# FEATURING:
## braces

Use `{`, `;` and `}` instead of indentation! Indentation and newlines in the source files will be ignored. e.g.:

```nestpy
n = input('Enter Number: ');
if (n % 2 == 0) {
	print('n is even')
} else {
	print('n is odd')
}
```
*(to be continued)*

---
github : https://github.com/slycedf/nestpy 
  
pypi : https://pypi.org/project/nestpython
