import tomllib
from pathlib import Path

from textual import work
from textual.reactive import reactive
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Footer

from rye_tui.components.mainframe import MainFrame
from rye_tui.components.helper_widgets import RyeHeader
from rye_tui.utils import rye_version
from rye_tui.config import RyeTuiConfig


class RyeTui(App):
    CSS_PATH = Path("assets/tui.css")

    cfg: RyeTuiConfig = RyeTuiConfig()
    active_project = reactive("")
    active_project_path = reactive("")
    active_project_toml = reactive({})
    active_project_lock = reactive([])

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
        self.active_project = ""
        self.active_project_path = ""
        self.app.query_one("#project_preview").content_info.clear()
        self.query_one("#project_preview").content_info.write("please select a file")
