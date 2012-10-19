class Module (object):
    def __init__ (self, adapter, regs):
        self.adapter, self.regs = adapter, regs
        self.poll_cache = None

        self.input_num    = adapter.hw.read_sr (regs.input_bit_size)
        if self.input_num:
            self.input_start  = adapter.hw.read_sr (regs.input_bit_start)

        self.output_num   = adapter.hw.read_sr (regs.output_bit_size)
        if self.output_num:
            self.output_start = adapter.hw.read_sr (regs.output_bit_start)

    def __str__ (self):
        return self.adapter.hw.read_string (self.regs.product_name, 73)

    def __repr__ (self):
        return str(self)

    def __getitem__ (self, bit):
        return self.get (bit)

    def __setitem__ (self, bit, high):
        return self.set (bit, high)

    def _ensure_valid_bit (fn):
        def __ensure_valid_bit (self, bit, *args, **kwargs):
            if bit < 0 or bit >= (self.input_num + self.output_num):
                raise ValueError ("Bit out of range")
            
            return fn (self, bit, *args, **kwargs)
        return __ensure_valid_bit

    @_ensure_valid_bit
    def is_output (self, bit):        
        return bit >= self.input_num

    @_ensure_valid_bit
    def get (self, bit):
        if self.is_output (bit):
            return self.adapter.hw.read_coils (self.output_start + bit).bits[0]
        else:
            return self.adapter.hw.read_discrete_inputs (self.input_start + bit).bits[0]

    @_ensure_valid_bit
    def set (self, bit, high=True):
        if not self.is_output (bit):
            raise ValueError ("Cannot set an input bit")

        self.adapter.hw.write_coil (self.output_start + bit, high)

    def get_all (self):
        i, o = [], []

        if self.input_num:
            i = self.adapter.hw.read_discrete_inputs (self.input_start, self.input_num).bits

        if self.output_num:
            o = self.adapter.hw.read_coils (self.output_start, self.output_num).bits

        return i + o

    def poll_prepare (self):
        self.poll_cache = self.get_all ()
        return self.poll_cache

    def poll (self):
        state = self.get_all ()

        ret = [(i, s) for (i, (s, c)) in enumerate (zip (state, self.poll_cache)) if s != c]
        self.poll_cache = state
        return ret
