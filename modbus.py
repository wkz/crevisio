import struct
import time

import pymodbus.register_read_message as rrm

try:
    from pymodbus.client import ModbusTcpClient
except ImportError:
    from pymodbus.client.sync import ModbusTcpClient

class CrevisModbus (ModbusTcpClient):
    def read_sr (self, reg, maxlen=1):
        r = None
        tryCount = 5
        while(tryCount > 0 and
              type(r) != rrm.ReadHoldingRegistersResponse):

            r = self.read_holding_registers (reg, count=maxlen)
            if type(r) != rrm.ReadHoldingRegistersResponse:
                time.sleep(0.5)

            tryCount -= 1

        if type (r) != rrm.ReadHoldingRegistersResponse:
            print("READ FAIL: %#x(%d)" % (reg, maxlen))
            return None

        if maxlen == 1:
            return r.registers[0]

        return r.registers

    def read_string (self, reg, maxlen):
        rs = self.read_sr (reg, (maxlen >> 1))

        if not rs:
            return None

        return struct.pack (">%dH" % len(rs[1:]), *rs[1:])[:rs[0]]
