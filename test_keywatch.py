import threading
import time
import unittest
import uuid
from types import SimpleNamespace
from unittest.mock import Mock, patch

import dictate
import keywatch


class KeyWatchTests(unittest.TestCase):
    def test_failed_native_wait_exits_instead_of_spinning(self):
        watch = keywatch.KeyWatch(threading.Event())
        with patch.object(
            keywatch.user32, "MsgWaitForMultipleObjects", return_value=keywatch.WAIT_FAILED
        ):
            with self.assertRaises(OSError):
                watch.pump()

    def watch(self):
        wake = threading.Event()
        found = keywatch.KeyWatch(wake, name="DictateTest" + uuid.uuid4().hex)
        self.assertTrue(found.start(), "Raw Input should register for a message-only window")
        self.addCleanup(found.stop)
        return wake, found

    def test_idle_watcher_stays_quiet_then_wakes_on_a_key_message(self):
        wake, found = self.watch()
        time.sleep(0.3)
        if not found.heard:  # a real keystroke during the test legitimately wakes it
            self.assertFalse(wake.is_set())
        wake.clear()
        keywatch.user32.PostMessageW(found.hwnd, keywatch.WM_INPUT, 0, 0)
        self.assertTrue(wake.wait(2))

    def test_stop_ends_the_thread(self):
        _, found = self.watch()
        found.stop()
        found.thread.join(2)
        self.assertFalse(found.thread.is_alive())
        self.assertFalse(found.active)


class WatcherLoopTests(unittest.TestCase):
    def watcher(self, raw_input_active):
        app = dictate.App.__new__(dictate.App)
        app.cfg = {"hotkey_key1": "right ctrl", "hotkey_key2": "right alt", "max_seconds": 60}
        app.state = dictate.IDLE
        app.pressed_at = 0.0
        app.stop_combo_poll = threading.Event()
        app.wake = Mock()
        app.keywatch = SimpleNamespace(active=raw_input_active)
        app.on_press = Mock()
        app.on_release = Mock()
        app.notify = Mock()
        passes = []

        def stop_after_three(*_):
            passes.append(1)
            if len(passes) >= 3:
                app.stop_combo_poll.set()

        return app, passes, stop_after_three

    def test_idle_watcher_sleeps_until_a_key_changes_instead_of_polling(self):
        app, passes, stop = self.watcher(raw_input_active=True)
        app.wake.wait.side_effect = stop
        pressed = patch("dictate.hotkeys.is_pressed", return_value=False)
        with pressed, patch.object(app.stop_combo_poll, "wait") as poll:
            app.hook_keys()
            app.combo_thread.join(2)
        self.assertEqual(len(passes), 3)
        app.wake.wait.assert_called_with(dictate.KEY_IDLE_SECONDS)
        poll.assert_not_called()

    def test_held_keys_are_watched_every_twenty_milliseconds(self):
        app, passes, stop = self.watcher(raw_input_active=True)
        pressed = patch("dictate.hotkeys.is_pressed", return_value=True)
        with pressed, patch.object(app.stop_combo_poll, "wait", side_effect=stop) as poll:
            app.hook_keys()
            app.combo_thread.join(2)
        poll.assert_called_with(0.02)
        app.wake.wait.assert_not_called()
        app.on_press.assert_called_once()

    def test_without_raw_input_the_watcher_still_polls(self):
        app, passes, stop = self.watcher(raw_input_active=False)
        pressed = patch("dictate.hotkeys.is_pressed", return_value=False)
        with pressed, patch.object(app.stop_combo_poll, "wait", side_effect=stop) as poll:
            app.hook_keys()
            app.combo_thread.join(2)
        poll.assert_called_with(0.02)
        app.wake.wait.assert_not_called()


if __name__ == "__main__":
    unittest.main()
