import threading
from tkinter import filedialog
from tkinter.ttk import Button

from hdrify import ssaProcessor


class FileSelectionButton(Button):
    def __init__(self, master, **kwargs):
        super().__init__(master, text="Select file and convert", **kwargs)
        self.configure(command=self._on_click)

    def _on_click(self) -> None:
        """Open file dialog and convert selected subtitle files."""
        files = filedialog.askopenfilenames(filetypes=[('ASS files', '.ass .ssa'),
                                                       ('all files', '.*')])
        if not files:
            return

        self.configure(state='disabled')

        def worker():
            try:
                for f in files:
                    print(f"Converting file: {f}")
                    ssaProcessor(f)
            finally:
                self.after(0, lambda: self.configure(state='normal'))

        threading.Thread(target=worker, daemon=True).start()
