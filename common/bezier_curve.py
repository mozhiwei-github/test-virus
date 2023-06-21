from math import pow
from numpy import linspace

"""贝塞尔曲线"""


class BezierCurve:
    def __init__(self, c1=(0, 0), c2=(1, 1), begin=(0, 0), end=(1, 1)):
        self.c1 = c1
        self.c2 = c2
        self.begin = begin
        self.end = end

    def _bezier_func(self, p, t, targ):
        return self.begin[p] * pow(1 - t, 3) + self.c1[p] * 3 * t * pow(1 - t, 2) + self.c2[p] * 3 * (
                1 - t) * pow(t, 2) + self.end[p] * pow(t, 3) - targ

    def _delta_bezier_func(self, p, t, targ):
        dt = 1e-8
        return (self._bezier_func(p, t, targ) - self._bezier_func(p, t, targ)) / dt

    def get_x(self, y):
        t = .5
        for i in range(0, 1000):
            t = t - self._bezier_func(1, t, y) / self._delta_bezier_func(1, t, y)
            if self._bezier_func(1, t, y) == 0:
                break
        return self._bezier_func(0, t, 0)

    def get_y(self, x):
        t = .5
        for i in range(0, 1000):
            t = t - self._bezier_func(0, t, x) / self._delta_bezier_func(0, t, x)
            if self._bezier_func(0, t, x) == 0:
                break
        return self._bezier_func(1, t, 0)

    def get(self, t):
        return self._bezier_func(0, t, 0), self._bezier_func(1, t, 0)


def bezier_curve_gen(start, end, dv=10):
    """贝塞尔曲线坐标生成器"""
    arg = (.17, .67, .83, .67)
    trange = linspace(0, 1, dv)  # 时间区间
    del_x = abs(end[0] - start[0])
    del_y = abs(end[1] - start[1])
    cb_x = BezierCurve((del_x * arg[0], del_x * arg[1]), (del_x * arg[2], del_x * arg[3]), end=(del_x, del_x))
    cb_y = BezierCurve((del_y * arg[0], del_y * arg[1]), (del_y * arg[2], del_y * arg[3]), end=(del_y, del_y))
    fg_x = 1 if start[0] < end[0] else -1
    fg_y = 1 if start[1] < end[1] else -1
    for t in trange:  # 这里是返回一个生成器
        yield (int(cb_x.get(t)[0] * fg_x + start[0]), int(cb_y.get(t)[0] * fg_y + start[1]))
