# rye-tui

> Rye meets Textual. Manage your python projects with a Tui

rye-tui is a CLI tool to manage your project rye projects. It offers a user interface to interact with your projects.

## Installation

Currently still in development, you can already install a first release with one of the three options:

```bash
pip install rye-tui
```

```bash
pipx install rye-tui
```

```bash
rye install rye-tui
```

## Usage

Once installed, you can open the tui with
```bash
trye
```

On first execution a configuration file is created, after that you have to use it again to get into the tui view.

![demo_image](https://raw.githubusercontent.com/Zaloog/rye-tui/main/images/image_rye_demo_preview.png)



* License: MIT

# TODOS:
- projects tab
    - project_preview
        - [ ] added dependencies
    - project_list
        - [ ] further check if folder is actually a rye project (based on .python-version?)
        - [ ] delete button functionality
            - [ ] delete folder
            - [ ] modal confirm screen
        - [ ] make buttons disappear, if project is not selected
        - [ ] edit button functionality
            -[ ] open pyproject.toml in modal
    - button functionalities
        - [ ] New Project
            - [X] update preview
            - [ ] extract path/options/name from command?
        - [ ] add/remove
            - [ ] modal with [Input of which package to add, DataTable for already present packages]
            - [ ] --dev functionality
            - [ ] Datatable view [package, synced, remove (Button)]
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
    - [ ] installed tools
    - [ ] installed toolchains
- config tab
    - [ ] source adding/removing
    - [ ] helper widget [label, input/switch/dropdown] + css update
- other stuff
    - [ ] focus widget color?
    - [ ] publish first version
