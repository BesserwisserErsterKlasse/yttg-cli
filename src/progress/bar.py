from dataclasses import dataclass, field

from rich.progress import Progress, TaskID


@dataclass(slots=True)
class ProgressBar:
    __progress: Progress = field(default_factory=Progress, init=False)
    __current_task: TaskID | None = field(default=None, init=False)

    @property
    def is_started(self) -> bool:
        """Whether the progress bar is started."""

        return self.__current_task is not None

    def start(self, total: int) -> None:
        """Start the progress bar."""

        self.__progress.start()
        self.__current_task = self.__progress.add_task('Downloading', total=total)

    def update(self, current: int) -> None:
        """Update progress bar."""

        assert self.__current_task is not None
        self.__progress.update(self.__current_task, completed=current)

    def stop(self) -> None:
        """Stop progress bar."""

        self.__progress.stop()
        self.__current_task = None
