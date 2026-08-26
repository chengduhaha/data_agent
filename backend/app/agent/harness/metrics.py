"""In-memory harness metrics exported as Prometheus text."""

from __future__ import annotations

from collections import defaultdict
from threading import Lock

_lock = Lock()
_counters: dict[str, dict[tuple[tuple[str, str], ...], float]] = defaultdict(
    lambda: defaultdict(float)
)
_histograms: dict[str, list[float]] = defaultdict(list)


def inc(name: str, amount: float = 1.0, **labels: str) -> None:
    key = tuple(sorted(labels.items()))
    with _lock:
        _counters[name][key] += amount


def observe(name: str, value: float) -> None:
    with _lock:
        _histograms[name].append(value)


def render_prometheus() -> str:
    lines: list[str] = []
    with _lock:
        for name, series in sorted(_counters.items()):
            for labels, value in series.items():
                if labels:
                    rendered = ",".join(f'{k}="{v}"' for k, v in labels)
                    lines.append(f"{name}{{{rendered}}} {value}")
                else:
                    lines.append(f"{name} {value}")
        for name, values in sorted(_histograms.items()):
            if not values:
                continue
            lines.append(f"{name}_count {len(values)}")
            lines.append(f"{name}_sum {sum(values)}")
    return "\n".join(lines) + ("\n" if lines else "")


def reset_metrics() -> None:
    with _lock:
        _counters.clear()
        _histograms.clear()
