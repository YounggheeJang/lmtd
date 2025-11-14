import math
from smithery.server import Server, tool
#from lmtd import calc_lmtd

def calc_lmtd(thi, tho, tci, tco):
    d1 = thi - tco
    d2 = tho - tci
    if d1 <= 0 or d2 <= 0:
        raise ValueError("Temperature differences must be positive.")
    if abs(d1 - d2) < 1e-12:
        return d1
    return (d1 - d2) / math.log(d1 / d2)

def create_server():
    server = Server(name="lmtd-calculator")

    @tool(server)
    def compute_lmtd(thi: float, tho: float, tci: float, tco: float):
        return {"lmtd": calc_lmtd(thi, tho, tci, tco)}

    return server
