"""Initialized-app regression: posted work reaches Tk without its fallback timer."""

import threading
import unittest
from unittest.mock import Mock, patch

import dictate as application


class DispatchTests(unittest.TestCase):
    def test_initialized_app_dispatches_worker_post_on_gui_thread(self):
        with (
            patch.object(application.settings, "load", return_value={}),
            patch.object(application.App, "_seed_recents"),
            patch.object(application, "Recorder", return_value=Mock()),
            patch.object(application.pystray, "Icon", return_value=Mock()),
        ):
            app = application.App()
        gui_thread = threading.get_ident()
        calls = []
        returned = threading.Event()

        def action():
            calls.append(threading.get_ident())
            app.root.quit()

        def worker():
            app.post(action)
            returned.set()

        thread = threading.Thread(target=worker)
        try:
            app.root.after(0, thread.start)
            timeout = app.root.after(2000, app.root.quit)
            app.root.mainloop()
            app.root.after_cancel(timeout)
            self.assertEqual(calls, [gui_thread])
            self.assertTrue(returned.wait(0.5))
        finally:
            app.root.destroy()
            thread.join(2)
