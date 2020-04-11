from pymirobot.MirobotClient import MirobotClient


class AnnRemoteControl():

    RANGE = {
        "x": (-100, 160),
        "y": (-30, 70),
        "z": (-170, 60),
        "a": (-180, 180), #+/- 360
        "b": (-200, 30),
        "c": (-180, 180), #+/- 360
    }

    def __init__(self, limit_file=None, host="mirobot"):
        self._set_file_limits(limit_file)

        self.miro = MirobotClient(host)
        self.miro.connect()
        self.miro.home_simultaneous()

    def go_to_axis(self, x, y, z, a, b, c, speed):
        x, y, z, a, b, c = self._get_limited_pos(x=x, y=y, z=z, a=a, b=b, c=c)

        self.miro.go_to_axis(x, y, z, a, b, c, speed)
        
    def go_to_axis_fraction(self, x, y, z, a, b, c, speed=2000):
        x, y, z, a, b, c = self._get_limited_pos_from_fractions(x=x, y=y, z=z, a=a, b=b, c=c)
        self.miro.go_to_axis(x, y, z, a, b, c, speed)
        

    def _set_file_limits(self, limit_file):
        self.limits = AnnRemoteControl.RANGE

        if limit_file:
            limits = __import__(limit_file, fromlist=[limit_file]).limits

            for axis, axis_range in AnnRemoteControl.RANGE.items():
                axis_limits = limits[axis]

                min_limit = max(axis_limits[0], axis_range[0])
                max_limit = min(axis_limits[1], axis_range[1])

                self.limits[axis] = (min_limit, max_limit)

    def _get_limited_pos(self, **kwargs):
        result = []
        
        for arg, val in kwargs.items():
            limits = self.limits[arg]

            limited = max(limits[0], min(limits[1], val))
            result.append(limited)
            
    def _get_limited_pos_from_fractions(self, **kwargs):
        result = []
        
        for arg, val in kwargs.items():
            limits = self.limits[arg]
            
            limited_range = limits[1] - limits[0]
            val_clamped = min(1., max(0., val))
            pos = limits[0] + val_clamped * limited_range
            print(pos)
            result.append(pos)

        return result
