import struct


import pymodbus.client.sync
import pymodbus.register_read_message


class CrevisModbus (pymodbus.client.sync.ModbusTcpClient):
    def read_sr (self, reg, maxlen=1):
        r = self.read_holding_registers (reg, count=maxlen)

        if type (r) != pymodbus.register_read_message.ReadHoldingRegistersResponse:
            print "READ FAIL: %#x(%d)" % (reg, maxlen)
            return None
        
        if maxlen == 1:
            return r.registers[0]

        return r.registers

    def read_string (self, reg, maxlen):
        rs = self.read_sr (reg, (maxlen >> 1))

        if not rs:
            return None

        return struct.pack (">%dH" % len(rs[1:]), *rs[1:])[:rs[0]]
