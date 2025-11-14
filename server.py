import math
from smithery.server import Server, tool
from lmtd import calc_lmtd

def create_server():
    server = Server(name="lmtd-calculator")

    @tool(server)
    def compute_lmtd(thi: float, tho: float, tci: float, tco: float):
        return {"lmtd": calc_lmtd(thi, tho, tci, tco)}

    return server
