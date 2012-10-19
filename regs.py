RESERVED = None

class RegisterMap (object):
    def __init__ (self, base, regs):
        self.base = base
        self.regs = {}

        offset = 0
        for (reg, size) in regs:
            if reg != RESERVED:
                self.regs[reg] = offset

            offset += size
        self.size = offset

    def __getattr__ (self, attr):
        if attr not in self.regs:
            return None

        return self.base + self.regs[attr]

    def __repr__ (self):
        regs = list (self.regs.iteritems ())
        regs.sort (key=lambda x: x[1])

        ret = "RegisterMap(base: %#x, size: %#x):\n" % (self.base, self.size)
        for (reg, addr) in regs:
            ret += "\t%s:\t%#x\n" % (reg, self.base + addr)

        return ret

adapter_id = RegisterMap (0x1000, (
        ("vendor_id", 1),
        ("device_type", 1),
        ("product_code", 1),
        ("firmware_rev", 1),
        ("serial", 1),
        ("product_name", 1),
        ("eeprom_sum", 1),
        (RESERVED, 9),
        ("firmware_date", 1),
        ("manufact_date", 1),
        ("vendor_name", 1),
        (RESERVED, 11),
        ("composite_id", 1),
        (RESERVED, 1),
))

adapter_info = RegisterMap (0x1100, (
        (RESERVED, 2),
        ("input_word_start", 1),
        ("output_word_start", 1),
        ("input_word_size", 1),
        ("output_word_size", 1),
        ("input_bit_start", 1),
        ("output_bit_start", 1),
        ("input_bit_size", 1),
        ("output_bit_size", 1),
        (RESERVED, 4),
        ("na_number", 1),
        (RESERVED, 1),
        ("slot_num", 1),
        ("slot_active_num", 1),
        ("slot_inactive_num", 1),
        ("adapter_id", 1),
        ("input_mode", 1),
        ("output_mode", 1),
        ("slot_inactive_map", 1),
        ("slot_live_map", 1),
        ("slot_alarm_map", 1),
        (RESERVED, 7),
))

slot_info = [RegisterMap (base, (
        ("product_id", 1),
        ("slot_io_code", 1),
        ("input_word_start", 1),
        ("output_word_start", 1),
        ("input_word_offset", 1),
        ("output_word_offset", 1),
        ("input_bit_start", 1),
        ("output_bit_start", 1),
        ("input_bit_size", 1),
        ("output_bit_size", 1),
        ("input_read", 1),
        ("output_read_write", 1),
        ("slot_inactive", 1),
        (RESERVED, 1),
        ("st_number", 1),
        ("product_name", 1),
        ("param_size", 1),
        ("param_read_write", 1),
        ("mem_size", 1),
        ("mem_read_write", 1),
        ("mem_read_write_offset", 1),
        ("product_code", 1),
        ("catalog_num", 1),
        ("firmware_rev", 1),
        ("fubus_rev", 1),
        (RESERVED, 7),
)) for base in range (0x2000, 0x2400, 0x20)]

