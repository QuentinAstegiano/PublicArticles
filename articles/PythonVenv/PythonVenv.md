# Python : Virtual Environnements

## Summary

On that article, I'll : 
* explain why you should use virtual environnements in Python
* show you the basic commands to create and use a virtual environnements

## Why using a virtual environnement ?

When working with any dev project, you'll depend on a lot of external librairies. 
In a lot of language, the dependencies are scoped to the project. For example, with Java, you'll use Maven or Gradle to express the required dependencies. In Python, the dependencies are installed globally.

I see two main drawbacks to that approach :
* Because everything is available to all your projects, you won't know precisely what is truly required for each one
* If multiple projects require the same dependency with different versions, then all hell break loose

The best Python way to handle dependency in the project scope is to use [venv](https://docs.python.org/3/library/venv.html)

*venv* will allow you to manage a localized python environnement, with its dependencies and specific configurations.
It'll scope your python to your project.

## Pre requisite

This guide apply to Python 3, version 3.6 and above.
*venv* is included in python3.

Note than in ubuntu, you'll need to install a specific package :
> sudo apt install python3-venv

## venv how-to

Let's start with an empty folder : 
> $ mkdir my_app
> $ cd my_app

If I check the current available packages, I'll find... quite a lot of things.
> $ pip freeze
> argcomplete==2.0.0
> Babel==2.10.3
> bcrypt==3.2.2
> blinker==1.6.2
> Brlapi==0.8.4
> certifi==2022.9.24
> chardet==5.1.0
> click==8.1.6
> colorama==0.4.6
> command-not-found==0.3
> cryptography==38.0.4
> cupshelpers==1.0
> dbus-python==1.3.2
> ...

You get the idea.
Now, lets create a virtual environnement.

> $ python3 -m venv .venv

Here, I'm creating a new virtual environnement, using venv ; and I tell python to store all the environnement related files in the *.venv* folder.

The environnement then need to be activated before it can be used

On linux
> $ source .venv/bin/activate

On Windows
> .\.venv\activate.bat

Once the env is activated, let's check what is available : 

> $ pip freeze
>

Nothing ! Great !

Now let's install a random dependency :
> $ pip install requests
> Collecting requests
> ...

And let's check :
> $ pip freeze
> certifi==2023.11.17
> charset-normalizer==3.3.2
> idna==3.6
> requests==2.31.0
> urllib3==2.1.0

Everything is working as intended : only the specified dependency (and it's transitive dependencies) are available in that environnement.

The last common command that you'll need aim to exit the virtual environnement.
That's as easy as the rest :

> $ deactivate

