Code Factory
==================

Code factory is a python tool for native code building, testing and deploying. It connect with some famous C/C++ build tools and Github platform. 

We use tools listed below:

- GCC/Clang for C/C++ compiler
- CMake with makefile or ninja or VS or xcode
- Google Test for testing
- Git and Github for code version contorl
- Travis CI and AppVeyor for all platform building and testing
- Github Release for deploy code
- conan for package manager

It's an easy use tools, and can be used to get the newest build tools

Some actions are support:

- init: initialize the code repository
- build: for running CMake build in one action
- clean: clean all middle files
- depclean: clean all with release file
- install: install a new C/C++ package with conan
- run: run the default executable file
