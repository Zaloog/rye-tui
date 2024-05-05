# rye-tui

> Rye meets Textual. Manage your python projects with a Tui

Describe your project here.
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