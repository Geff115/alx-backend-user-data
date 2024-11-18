0x03. User authentication service
Back-end
Authentification
 Weight: 1


Requirements:

    - Allowed editors: vi, vim, emacs
    - All my files will be interpreted/compiled on Ubuntu 18.04 LTS using python3 (version 3.7)
    - The first line of all my files should be exactly #!/usr/bin/env python3
    - My code should use the pycodestyle style (version 2.5)
    - I should use SQLAlchemy 1.3.x
    - The length of my files will be tested using wc
    - All my modules should have a documentation (python3 -c 'print(__import__("my_module").__doc__)')
    - All my classes should have a documentation (python3 -c 'print(__import__("my_module").MyClass.__doc__)')
    - All my functions (inside and outside a class) should have a documentation (python3 -c 'print(__import__("my_module").my_function.__doc__)' and python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)')
    - All my functions should be type annotated
    - The flask app should only interact with Auth and never with DB directly.
    - Only public methods of Auth and DB should be used outside these classes


Setup:

    You will need to install bcrypt

    pip3 install bcrypt