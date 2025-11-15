from mcp.server.fastmcp import Context, FastMCP
from smithery.decorators import smithery
from pydantic import BaseModel, Field
from typing import Literal, Optional
import math

class ConfigSchema(BaseModel):
    unit: str = Field("celsius", description="Temperature unit (celsius or fahrenheit)")

def _lmtd_from_diffs(d1: float, d2: float) -> float:
    if d1 <= 0 or d2 <= 0:
        raise ValueError("Temperature differences must be positive values.")
    if abs(d1 - d2) < 1e-12:
        return d1
    return (d1 - d2) / math.log(d1 / d2)

@smithery.server(config_schema=ConfigSchema)
def create_server():

    server = FastMCP(name="lmtd Server")

    @server.tool()
    def compute_lmtd(thi: float, tho: float, tci: float, tco: float, flow_type: Optional[Literal["counter", "parallel"]] = "counter", ctx: Optional[Context] = None) -> dict:
        """
        LMTD 계산기 (Tool)
        파라미터:
          - thi: hot stream inlet temperature
          - tho: hot stream outlet temperature
          - tci: cold stream inlet temperature
          - tco: cold stream outlet temperature
          - flow_type: "counter" 또는 "parallel" (기본: counter)
        반환:
          { "lmtd": float, "units": str, "flow_type": str }
        """
        units = "celsius"
        if ctx is not None:
            try:
                units = ctx.session_config.unit or units
            except Exception:
                pass

        if flow_type == "counter":
            d1 = thi - tco
            d2 = tho - tci
        elif flow_type == "parallel":
            d1 = thi - tci
            d2 = tho - tco
        else:
            raise ValueError("flow_type must be 'counter' or 'parallel'")

        lmtd_val = _lmtd_from_diffs(d1, d2)
        return {"lmtd": round(lmtd_val, 9), "units": units, "flow_type": flow_type}

    return server
