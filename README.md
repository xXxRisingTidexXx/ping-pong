# ping-pong

It's a classic 2D game, where you're to hit the ball using the paddle.

## Installation

In the project root create and enable a [virtual environment](https://docs.python.org/3/tutorial/venv.html).

```
virtualenv venv
source venv/bin/activate
```

Then install the system package required to enable Tcl / Tk interpreter. The provided installation is made for
Debian-based distros, but there are examples for
[Arch Linux](https://bbs.archlinux.org/viewtopic.php?id=224553),
[CentOS](https://stackoverflow.com/questions/40588444/how-to-install-python3-tk-in-centos/48475653), etc.

```
sudo apt-get install python3-tk
```

After that install a library for media interaction.

```
pip install pygame
```

## Usage

Being in virtual environment, run this.

```
python pingpong.py
```
