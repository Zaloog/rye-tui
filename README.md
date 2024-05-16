
[![Rye](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/rye/main/artwork/badge.json)](https://rye-up.com)
[![PyPI-Server](https://img.shields.io/pypi/v/rye-tui.svg)](https://pypi.org/project/rye-tui/)
[![Pyversions](https://img.shields.io/pypi/pyversions/rye-tui.svg)](https://pypi.python.org/pypi/rye-tui)
[![Licence](https://img.shields.io/pypi/l/rye-tui.svg)](https://github.com/astral-sh/rye-tui/blob/main/LICENSE)
[![Downloads](https://static.pepy.tech/badge/rye-tui)](https://pepy.tech/project/rye-tui)

# rye-tui

> Rye meets Textual. Manage your python projects with a Tui

rye-tui is a CLI tool to manage your [rye] projects. It offers a UI to interact with your projects.

## Currently still under development
A 0.1.0 version is already released on PyPi

## Installation

You can already install a first release with one of the three options:

```bash
pip install rye-tui
```

```bash
pipx install rye-tui
```

```bash
rye install rye-tui
```
I recommend using [pipx] or [rye] to install CLI Tools into an isolated environment.

## Usage

Once installed, you can open the tui with
```bash
trye
```

On first execution a configuration file is created. Afterwards you can run `trye` again to get into the tui view.

The configuration file contains a list of the paths of your rye-managed pojects.
Also a project home directory is defined (default: `HOMEPATH`), which helps initializing new projects under a certain location.

Rye-Tui is following the [XDG] basedir-spec. Therefore the configuration file is located under your OS specific `config_user_dir`.

![demo_image](https://raw.githubusercontent.com/Zaloog/rye-tui/main/images/image_rye_demo_preview.png)



* License: MIT

# TODOS:
- projects tab
    - project_preview
        - [X] added dependencies
        - [ ] make view nicer
    - project_list
        - [ ] further check if folder is actually a rye project (based on .python-version?)
        - [X] delete button functionality
            - [X] delete folder
            - [X] modal confirm screen
        - [X] make buttons disappear, if project is not selected
        - [ ] edit button functionality
            -[ ] open pyproject.toml in modal
    - button functionalities
        - [ ] New Project
            - [X] update preview
            - [ ] extract path/options/name from command, add flags?
        - [X] add/remove
            - [X] modal with [Input of which package to add, DataTable for already present packages]
            - [X] --dev functionality, maybe other color/additional column
                - [x] --dev functionality remove package
                - [X] --dev packages display
            - [X] Datatable view [package, synced, remove (Button)]
        - [X] sync
            - [X] update preview
        - [X] pin python version
            - [X] update preview
        - [ ] build
        - [ ] publish when wheels in dist/*
- general tab
    - [ ] Add Rye Project Home from config.ini
        - [x] Functionality added
        - [ ] Input Validator for Path, ' ' in Path?
    - [X] installed tools
    - [X] installed toolchains
- config tab
    - [ ] source adding/removing
    - [ ] helper widget [label, input/switch/dropdown] + css update
- other stuff
    - [ ] focus widget color?
    - [ ] Docs/Readme
    - [X] publish first version


[XDG]: https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
[platformdirs]: https://platformdirs.readthedocs.io/en/latest/
[textual]: https://textual.textualize.io
[pipx]: https://github.com/pypa/pipx
[rye]: https://rye-up.com
