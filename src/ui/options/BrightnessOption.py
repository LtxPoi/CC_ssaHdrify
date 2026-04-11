from __future__ import annotations

import tkinter
from ttkbootstrap import Frame, Label, Entry

import i18n
from conversion_setting import config

_BRIGHTNESS_REC_KEYS = {"PQ": "brightness_rec_pq", "HLG": "brightness_rec_hlg"}


def validateBrightness(newBrightness):
    """Validate-only: does NOT mutate config (read happens at conversion time)."""
    if newBrightness == '':
        return True
    if not newBrightness.isdecimal():
        return False
    return 1 <= int(newBrightness) <= 10000


class BrightnessOption(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure(1, weight=1)

        self._label = Label(master=self, text=i18n.get("brightness_label"))
        self._label.grid(row=0, column=0, sticky=tkinter.W)

        self.target_brightness_var = tkinter.StringVar()
        self.target_brightness_var.set(config.targetBrightness)
        validate_brightness_wrapper = (self.register(validateBrightness), '%P')
        target_brightness_input = Entry(master=self, textvariable=self.target_brightness_var, validate="key",
                                        validatecommand=validate_brightness_wrapper)
        target_brightness_input.grid(row=0, column=1, sticky=tkinter.EW)

        # Recommendation label (dynamic, follows EOTF selection)
        self._rec_label = Label(master=self, text=self._rec_text())
        self._rec_label.grid(row=1, column=0, columnspan=2, sticky=tkinter.W, pady=(8, 0))

    def _rec_text(self, eotf: str | None = None) -> str:
        """Return localized recommendation text for the given (or current) EOTF."""
        rec_key = _BRIGHTNESS_REC_KEYS.get((eotf or config.eotf).upper(), "brightness_rec_pq")
        return i18n.get(rec_key)

    def update_recommendation(self, eotf: str = "PQ"):
        """Update the recommendation text based on EOTF selection."""
        self._rec_label.configure(text=self._rec_text(eotf))

    def refresh_language(self):
        self._label.configure(text=i18n.get("brightness_label"))
        self._rec_label.configure(text=self._rec_text())
