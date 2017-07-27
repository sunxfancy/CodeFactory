Code Factory
==================

Code Factory is a python tool for native code building, testing and deploying. It connects with some famous C/C++ build tools and Github platform. 

We use tools listed below:

- GCC/Clang for C/C++ compiler
- CMake with makefile or ninja or VS or xcode
- Google Test for testing
- Git and Github for code version control
- Travis CI and AppVeyor for all platform building and testing
- Github Release for deploy code
- conan for the package manager

# Install

we recommand using pip to install our tool:

```sh
# using sudo in unix system
pip install codefactory

# or install in user directory
pip install codefactory --user

# test it
codef --help
```

# Actions

Some actions are supported:

- init: initialize the code repository
- build: for running CMake build in one action
- clean: clean all middle files
- depclean: clean all with release file
- install: install a new C/C++ package with conan
- run: run the default executable file


## Create a new C++ project

`init` command is used to create new project, adding project as args:

```sh
codef init new_project
cd new_project
```


## Build it

```sh
codef build
```