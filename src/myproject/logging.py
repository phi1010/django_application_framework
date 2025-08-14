import logging
from logging import Handler
import prometheus_client

COUNTER = prometheus_client.Counter(
    "metric_logging_total",
    "Total number of log messages",
    ["level", "logger", "levelnum"]
)
class MetricLoggingHandler(Handler):
    """
    Custom logging handler to capture metrics.
    """
    def __init__(self):
        super(MetricLoggingHandler, self).__init__()
        for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            COUNTER.labels(level, "root", logging.getLevelName(level))
    def emit(self, record):
        level = record.levelname
        levelnum = record.levelno
        loggername = record.name
        COUNTER.labels(level, loggername, levelnum).inc()