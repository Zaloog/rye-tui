
[![Rye](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/rye/main/artwork/badge.json)](https://rye-up.com)
[![PyPI-Server](https://img.shields.io/pypi/v/rye-tui.svg)](https://pypi.org/project/rye-tui/)
[![Pyversions](https://img.shields.io/pypi/pyversions/rye-tui.svg)](https://pypi.python.org/pypi/rye-tui)
[![Licence](https://img.shields.io/pypi/l/rye-tui.svg)](https://github.com/astral-sh/rye-tui/blob/main/LICENSE)
[![Downloads](https://static.pepy.tech/badge/rye-tui)](https://pepy.tech/project/rye-tui)

# rye-tui

> Rye meets Textual. Manage your python projects with a Tui

rye-tui is a CLI tool to manage your [rye] projects. It offers a UI to interact with your projects.

![header_image](https://raw.githubusercontent.com/Zaloog/rye-tui/main/images/image_rye_demo_preview.png)

## Currently still under development
A 0.2.0 version is already released on [PyPi]

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


## Features

Rye-Tui is divided into 3 Tabs:
1. Projects
2. General
3. Config

### Projects Tab
The Projects Tab holds all your rye projects and gives you an overview to each project based on the `pyproject.toml` and installed packages.
`Edit`- Button function to open pyproject.toml is still missing currently. 
![project_image](https://raw.githubusercontent.com/Zaloog/rye-tui/main/images/image_rye_project.png)

`rye add` and  `rye add --dev` is already supported, flags are still missing currently.
![add_image](https://raw.githubusercontent.com/Zaloog/rye-tui/main/images/image_rye_add.png)

### General Tab
The General Tab has an input field to define your project-home path, which acts as an default location, to easily create a new project there.
Furthermore you get an overview over your globally installed tools including version and available scripts.
The final section lists all installed toolchain.
![general_image](https://raw.githubusercontent.com/Zaloog/rye-tui/main/images/image_rye_general.png)

### Config Tab
The Config Tab can be used to change rye's underlying config.
![config_image](https://raw.githubusercontent.com/Zaloog/rye-tui/main/images/image_rye_config.png)

## Feedback and Issues
Feel free to reach out and share your feedback, or open an Issue, if something doesnt work as expected.
Also check the [Changelog](https://github.com/Zaloog/rye-tui/blob/main/CHANGELOG.md) for new updates.

## Open Points:
- [ ] edit button functionality for pyproject toml
- [ ] Button to go directly to Folder
- [ ] Support Flags for Rye Init and Rye add
- [ ] Support publishing
- [ ] Enable Rye Tool Management, like rye add
- [ ] Enable source removing
- [ ] Folder Scanner for rye projects

[XDG]: https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
[platformdirs]: https://platformdirs.readthedocs.io/en/latest/
[textual]: https://textual.textualize.io
[pipx]: https://github.com/pypa/pipx
[rye]: https://rye-up.com
[PyPi]: https://pypi.org/project/rye-tui/
