import tomllib
from pathlib import Path

from textual import work
from textual.reactive import reactive
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Footer

from rye_tui.components.mainframe import MainFrame
from rye_tui.components.helper_widgets import RyeHeader
from rye_tui.utils import rye_version, read_toml, read_lock
from rye_tui.config import RyeTuiConfig


class RyeTui(App):
    CSS_PATH = Path("assets/tui.css")

    cfg: RyeTuiConfig = RyeTuiConfig()
    project = reactive({"name": "", "path": "", "toml": {}, "lock": []})

    def compose(self) -> ComposeResult:
        self.add_cwd_to_config()

        yield RyeHeader()
        yield Footer()
        with Horizontal():
            yield MainFrame()
        return super().compose()

    @work(thread=True)
    def on_mount(self) -> None:
        self.title = "RyeTui"
        self.sub_title = rye_version()

    @work(thread=True)
    def add_cwd_to_config(self):
        project_path = Path().cwd().as_posix()
        if project_path not in self.cfg.project_paths:
            toml_path = Path().cwd() / "pyproject.toml"
            if toml_path.exists():
                with open(toml_path, "rb") as tomlfile:
                    project_infos = tomllib.load(tomlfile)

                project_name = project_infos["project"]["name"]
                self.cfg.add_project(
                    new_project_name=project_name, new_project_path=project_path
                )
                self.notify(
                    f"[blue]{project_name}[/] was added to [b]rye-tui[/b] config",
                    title="Project List Updated",
                )
            else:
                self.notify("[red]NO[/] pyproject.toml found in [blue]CWD[/]")

    def reset_project(self):
        self.project = {"name": "", "path": "", "toml": {}, "lock": []}
        preview_window = self.app.query_one("#project_preview")
        preview_window.content_info.clear()
        preview_window.content_info.write("please select a file")
        preview_window.border_subtitle = "no project selected"

    def get_project_infos(self, project_name):
        proj_dict = self.project
        proj_dict["name"] = project_name
        proj_dict["path"] = self.cfg.config["projects"].get(project_name)

        proj_dict["toml"] = read_toml(path=proj_dict["path"])

        proj_dict["lock"] = read_lock(path=proj_dict["path"])

        # if not proj_dict["lock"]:
        #     self.notify(
        #         title="File not found",
        #         message=f"[blue]requirements.lock[/] is not present yet for [blue]{self.app.project['name']}[/]",
        #         severity="error",
        #         timeout=1
        #     )
