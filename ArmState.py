import re


class ArmState:
    def __init__(
        self,
        active,
        angle_x,
        angle_y,
        angle_z,
        rail,
        angle_rx,
        angle_ry,
        angle_rz,
        cartesian_x,
        cartesian_y,
        cartesian_z,
        cartesian_rx,
        cartesian_ry,
        cartesian_rz,
        pwm1,
        pwm2,
        motion_mode,
    ):
        self.active = active
        self.a_x = angle_x
        self.a_y = angle_y
        self.a_z = angle_z
        self.rail = rail
        self.a_rx = angle_rx
        self.a_ry = angle_ry
        self.a_rz = angle_rz
        self.c_x = cartesian_x
        self.c_y = cartesian_y
        self.c_z = cartesian_z
        self.c_rx = cartesian_rx
        self.c_ry = cartesian_ry
        self.c_rz = cartesian_rz
        self.pwm1 = pwm1
        self.pwm2 = pwm2
        self.motion_mode = motion_mode

    @staticmethod
    def from_status_string(response_string):
        regex = (
            r"<(Idle|Run),"
            + r"[^:]+:([-0-9.]+),([-0-9.]+),([-0-9.]+),([-0-9.]+),([-0-9.]+),([-0-9.]+),([-0-9.]+),"
            + r"[^:]+:([-0-9.]+),([-0-9.]+),([-0-9.]+),([-0-9.]+),([-0-9.]+),([-0-9.]+),"
            + r"[^:]+:([0-9]+),[^:]+:([0-9]+),[^:]+:([0-9]+)>"
        )

        query = re.compile(regex)
        result = query.match(response_string)

        if result:
            groups = result.groups()

            running = groups[0] == "Run"
            angles = [float(angle) for angle in groups[1:14]]
            pwms = [int(pwm) for pwm in groups[14:16]]
            motion_mode = int(groups[16])  # todo

            return ArmState(running, *angles, *pwms, motion_mode)
        else:
            return None

    def __str__(self):
        return (
            f"Running={self.active}\n"
            + f"angle_x={self.a_x}, angle_y={self.a_y}, angle_z={self.a_z}\n"
            + f"rail={self.rail}\n"
            + f"angle_rx={self.a_rx}, angle_ry={self.a_ry}, angle_rz={self.a_rz}\n"
            + f"cartesian_x={self.c_x}, cartesian_y={self.c_y}, cartesian_z={self.c_z}\n"
            + f"cartesian_rx={self.c_rx}, cartesian_ry={self.c_ry}, cartesian_rz={self.c_rz}\n"
            + f"pwm1={self.pwm1}, pwm1={self.pwm2}, motion_mode={self.motion_mode}\n"
        )
