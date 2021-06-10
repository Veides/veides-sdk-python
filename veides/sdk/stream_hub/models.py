from datetime import datetime


class TrailTimestamp(datetime):
    @staticmethod
    def from_string(timestamp):
        return TrailTimestamp.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")

    def __str__(self):
        return self.strftime("%Y-%m-%dT%H:%M:%SZ")


class Trail(object):
    def __init__(self, name, value, timestamp):
        """
        :param name
        :type name: str
        :param value
        :type value: str|int|float
        :param timestamp
        :type timestamp: TrailTimestamp
        """
        if not isinstance(name, str):
            raise TypeError('Trail name should be a string')

        if len(name) == 0:
            raise ValueError('Trail name should be at least 1 length')

        if not any([isinstance(value, t) for t in [str, float, int]]):
            raise TypeError('Trail value should be one of: string, integer, float')

        if not isinstance(timestamp, TrailTimestamp):
            raise TypeError('Trail timestamp should be of type TrailTimestamp')

        self.name = name
        self.value = value
        self.timestamp = timestamp

    def __str__(self):
        return 'Trail(name={}, value={}, timestamp={})'.format(self.name, self.value, self.timestamp)
