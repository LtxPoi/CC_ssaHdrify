import threading
from tkinter import filedialog
from tkinter.ttk import Button

from conversion_setting import config
from hdrify import ssaProcessor


class FileSelectionButton(Button):
    def __init__(self, master, **kwargs):
        super().__init__(master, text="Select file and convert", **kwargs)
        self.configure(command=self._on_click)
        self._worker_thread = None

    def _on_click(self) -> None:
        """Open file dialog and convert selected subtitle files."""
        files = filedialog.askopenfilenames(filetypes=[('ASS files', '.ass .ssa'),
                                                       ('all files', '.*')])
        if not files:
            return

        self.configure(state='disabled')
        brightness = config.targetBrightness

        def worker():
            try:
                for f in files:
                    print(f"Converting file: {f}")
                    ssaProcessor(f, target_brightness=brightness)
            finally:
                self.after(0, lambda: self.configure(state='normal'))

        self._worker_thread = threading.Thread(target=worker, daemon=False)
        self._worker_thread.start()

    @property
    def is_converting(self) -> bool:
        return self._worker_thread is not None and self._worker_thread.is_alive()
