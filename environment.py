import random


class DisasterEnvironment:
    def __init__(self):
        self.severity_levels = ["LOW", "MODERATE", "HIGH", "CRITICAL"]

    def sense_environment(self):
        severity = random.choice(self.severity_levels)
        return {
            "event": "DisasterDetected",
            "severity": severity
        }
