from pymirobot.MirobotClient import MirobotClient
import importlib


class AnnRemoteControl:

    RANGE = {
        "x": (-100, 160),
        "y": (-30, 70),
        "z": (-170, 60),
        "a": (-180, 180),  # +/- 360
        "b": (-200, 30),
        "c": (-180, 180),  # +/- 360
    }

    def __init__(self, limit_file=None, host="mirobot"):
        self._set_file_limits(limit_file)

        self.miro = MirobotClient(host)
        self.miro.connect()
        self.miro.home_simultaneous()

    def get_arm_state(self):
        return self.miro.get_arm_state()

    def go_to_axis(self, x, y, z, a, b, c, speed):
        x, y, z, a, b, c = self._get_limited_pos(x=x, y=y, z=z, a=a, b=b, c=c)

        self.miro.go_to_axis(x, y, z, a, b, c, speed)

    def go_to_axis_fraction(self, x, y, z, a, b, c, speed=2000):
        active = True
        while active:
            state = None
            while not state:
                state = self.miro.get_arm_state()
            active = state.active

        x, y, z, a, b, c = self._get_limited_pos_from_fractions(
            x=x, y=y, z=z, a=a, b=b, c=c
        )
        self.miro.go_to_axis(x, y, z, a, b, c, speed)

    def get_current_axis_fraction(self):
        state = self.miro.get_arm_state()

        if state:
            x = AnnRemoteControl._get_limit_fraction_for_rotation(
                state.a_rx, self.limits["x"]
            )
            y = AnnRemoteControl._get_limit_fraction_for_rotation(
                state.a_ry, self.limits["y"]
            )
            z = AnnRemoteControl._get_limit_fraction_for_rotation(
                state.a_rz, self.limits["z"]
            )
            a = AnnRemoteControl._get_limit_fraction_for_rotation(
                state.a_x, self.limits["a"]
            )
            b = AnnRemoteControl._get_limit_fraction_for_rotation(
                state.a_y, self.limits["b"]
            )
            c = AnnRemoteControl._get_limit_fraction_for_rotation(
                state.a_z, self.limits["c"]
            )

            return (x, y, z, a, b, c)

        else:
            return None

    @staticmethod
    def _get_limit_fraction_for_rotation(value, axis_limits):
        offset = value - axis_limits[0]
        limit_range = axis_limits[1] - axis_limits[0]

        return offset / limit_range

    def _set_file_limits(self, limit_file):
        self.limits = AnnRemoteControl.RANGE

        if limit_file:
            limits = importlib.import_module(limit_file).limits

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
            val_clamped = min(1.0, max(0.0, val))
            pos = limits[0] + val_clamped * limited_range
            result.append(pos)

        return result
