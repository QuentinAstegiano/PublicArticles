# Python: Virtual Environments

## Summary

In this article, I will:
* Explain why you should use virtual environments in Python.
* Provide the basic commands to create and use virtual environments.

## Why Use a Virtual Environment?

When working on any development project, you will depend on numerous external libraries. In many languages, dependencies are scoped to the project. For instance, in Java, Maven or Gradle is used to express required dependencies. In Python, dependencies are installed globally.

I identify two main drawbacks to this approach:
* Since everything is available to all your projects, it's challenging to determine precisely what is required for each one.
* If multiple projects need the same dependency with different versions, chaos ensues.

The best Python approach to handle project-specific dependencies is to use [venv](https://docs.python.org/3/library/venv.html).

*venv* enables you to manage a localized Python environment with its dependencies and specific configurations, effectively scoping your Python to your project.

## Prerequisite

This guide applies to Python 3, version 3.6 and above.
*venv* is included in Python 3.

Note that in Ubuntu, you'll need to install a specific package:
> sudo apt install python3-venv

## venv How-To

Let's start with an empty folder:
> $ mkdir my_app
> $ cd my_app

If I check the currently available packages, I'll find... quite a lot of things.
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
Now, let's create a virtual environment.

> $ python3 -m venv .venv

Here, I'm creating a new virtual environment using venv, and I instruct Python to store all environment-related files in the *.venv* folder.

The environment then needs to be activated before it can be used.

On Linux:
> $ source .venv/bin/activate

On Windows:
> .\.venv\activate.bat

Once the env is activated, let's check what is available:

> $ pip freeze
>

Nothing! Great!

Now let's install a random dependency:
> $ pip install requests
> Collecting requests
> ...

And let's check:
> $ pip freeze
> certifi==2023.11.17
> charset-normalizer==3.3.2
> idna==3.6
> requests==2.31.0
> urllib3==2.1.0

Everything is working as intended: only the specified dependency (and its transitive dependencies) are available in that environment.

The last common command that you'll need aims to exit the virtual environment.
That's as easy as the rest:

> $ deactivate
