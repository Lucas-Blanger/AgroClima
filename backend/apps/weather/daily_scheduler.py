import json
import logging
import os
import threading
import time
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.utils import timezone

logger = logging.getLogger(__name__)

_scheduler_started = False
_scheduler_guard = threading.Lock()

_LOCK_MAX_AGE_SECONDS = 6 * 60 * 60
_SLEEP_SECONDS = 60


def start_daily_scheduler():
    global _scheduler_started

    with _scheduler_guard:
        if _scheduler_started:
            return

        thread = threading.Thread(
            target=_scheduler_loop,
            name="daily-data-updater",
            daemon=True,
        )
        thread.start()
        _scheduler_started = True
        logger.info("Daily data scheduler started.")


def _scheduler_loop():
    while True:
        try:
            _run_updates_if_due()
        except Exception:
            logger.exception("Unexpected error in daily scheduler.")

        time.sleep(_SLEEP_SECONDS)


def _run_updates_if_due():
    now_local = timezone.localtime()
    target_hour, target_minute = _read_target_time()
    today = now_local.date()

    if now_local.hour < target_hour:
        return
    if now_local.hour == target_hour and now_local.minute < target_minute:
        return
    if _read_last_run_date() == today.isoformat():
        return
    if not _acquire_lock_file():
        return

    try:
        if _read_last_run_date() == today.isoformat():
            return

        logger.info("Running automatic daily update for weather and news.")
        call_command("update_weather")
        call_command("update_news")
        _write_last_run_date(today.isoformat())
        logger.info("Automatic daily update finished successfully.")
    except Exception:
        logger.exception("Automatic daily update failed.")
    finally:
        _release_lock_file()


def _read_target_time():
    raw_time = getattr(settings, "DAILY_UPDATE_TIME", "06:00")
    try:
        parsed = datetime.strptime(raw_time, "%H:%M")
        return parsed.hour, parsed.minute
    except ValueError:
        logger.warning("Invalid DAILY_UPDATE_TIME=%s. Using fallback 06:00.", raw_time)
        return 6, 0


def _read_last_run_date():
    state_file = _state_file()
    if not state_file.exists():
        return None

    try:
        with state_file.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data.get("last_run_date")
    except Exception:
        logger.exception("Failed to read daily scheduler state file.")
        return None


def _write_last_run_date(last_run_date):
    state_file = _state_file()
    temp_file = state_file.with_suffix(".tmp")
    payload = {"last_run_date": last_run_date}

    with temp_file.open("w", encoding="utf-8") as file:
        json.dump(payload, file)

    os.replace(temp_file, state_file)


def _state_file():
    return Path(settings.BASE_DIR) / ".daily_update_state.json"


def _lock_file():
    return Path(settings.BASE_DIR) / ".daily_update.lock"


def _acquire_lock_file():
    lock_file = _lock_file()

    if lock_file.exists():
        try:
            age = time.time() - lock_file.stat().st_mtime
            if age > _LOCK_MAX_AGE_SECONDS:
                lock_file.unlink(missing_ok=True)
        except OSError:
            logger.exception("Failed to evaluate stale lock file.")
            return False

    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    try:
        fd = os.open(lock_file, flags)
        os.close(fd)
        return True
    except FileExistsError:
        return False
    except OSError:
        logger.exception("Failed to acquire lock file.")
        return False


def _release_lock_file():
    try:
        _lock_file().unlink(missing_ok=True)
    except OSError:
        logger.exception("Failed to release lock file.")
