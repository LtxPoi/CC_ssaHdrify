import queue
import tkinter
from ttkbootstrap import LabelFrame, Scrollbar


class QueueStream:
    """线程安全的文本输出流，写入底层 queue.Queue。

    实现了 write() / flush() 接口，可直接用于
    contextlib.redirect_stdout / redirect_stderr。
    消费即释放，无内存积累。
    """

    def __init__(self) -> None:
        self._queue: queue.Queue[str] = queue.Queue()

    def write(self, text: str) -> None:
        if text:
            self._queue.put(text)

    def flush(self) -> None:
        pass  # 满足 TextIO 接口，无需实际实现

    def get_nowait(self) -> str:
        """Non-blocking read; raises queue.Empty if nothing available."""
        return self._queue.get_nowait()


class MessageFrame(LabelFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.messageStream = QueueStream()
        self.callbackId = ""

        self._container = tkinter.Frame(master=self)
        self._container.pack(expand=True, fill='both')

        self.text = tkinter.Text(master=self._container, wrap='word')
        self._scrollbar = Scrollbar(self._container, orient='vertical', command=self.text.yview)
        self.text.configure(yscrollcommand=self._scrollbar.set)

        self._scrollbar.pack(side='right', fill='y')
        self.text.pack(side='left', expand=True, fill='both')

        self.updateText()

    _MAX_LINES = 2000

    def updateText(self):
        self.text.config(state=tkinter.NORMAL)
        try:
            while True:
                chunk = self.messageStream.get_nowait()
                self.text.insert(tkinter.END, chunk)
        except queue.Empty:
            pass
        # Trim old lines to prevent unbounded memory growth
        line_count = int(self.text.index("end-1c").split(".")[0])
        if line_count > self._MAX_LINES:
            self.text.delete("1.0", f"{line_count - self._MAX_LINES}.0")
        self.text.config(state=tkinter.DISABLED)
        self.text.see(tkinter.END)  # 自动滚动到最新消息
        self.callbackId = self.after(500, self.updateText)

    def stopPolling(self):
        """Cancel the pending after callback to prevent errors on window close."""
        if self.callbackId:
            self.after_cancel(self.callbackId)
            self.callbackId = ""
