import time
import threading

import crevisio.modbus as modbus
import crevisio.module as module
import crevisio.regs   as regs

class Adapter (object):
    def __init__ (self, host):
        self.slots = {}
        self.subs = []
        self._poll_lock = threading.Lock ()
        self._poll_thread = None
        self._poll_term = threading.Event ()

        self.host = host
        self.hw = modbus.CrevisModbus (host)

        vid = self.hw.read_sr (regs.adapter_id.vendor_id)
        if vid != 0x02e5:
            raise Exception ("%s does not appear to be a Crevis I/O adapter, got vendor id %#x" % (host, vid))

        live = self.hw.read_sr (regs.adapter_info.slot_live_map)
        for slot in [i for i in range (32) if live & (1 << i)]:
            self.slots[slot] = module.Module (self, regs.slot_info[slot])

    def __str__ (self):
        return "%s@%s" % (self.hw.read_string (regs.adapter_id.product_name, 34), self.host)

    def __repr__ (self):
        ret = str(self) + ":\n"

        for slot in self.slots:
            ret += "\tSlot %d: %s\n" % (slot, self.slots[slot])
        
        return ret

    def __getitem__ (self, slot):
        return self.slot (slot)

    def close (self):
        self._poll_lock.acquire ()

        self._poll_term.set ()
        self._poll_thread.join ()
        self._poll_term.clear ()

        self._poll_lock.release ()

    def slot (self, slot):
        if slot not in self.slots:
            return None

        return self.slots[slot]

    def poll (self):
        [self.slots[s].poll_prepare () for s in self.slots]
        return {s: self.slots[s].poll_cache for s in self.slots}

    def _poll (self, interval=0.5):
        while True:
            self._poll_lock.acquire ()

            states = {s: self.slots[s].poll () for s in self.slots}
            states = {s: states[s] for s in states if states[s]}

            if states:
                [c (states) for c in self.subs]

            self._poll_lock.release ()

            if self._poll_term.is_set ():
                break

            time.sleep (interval)

            if self._poll_term.is_set ():
                break

    def subscribe (self, callback):
        self._poll_lock.acquire ()
        self.subs.append (callback)

        if len(self.subs) == 1:
            [self.slots[s].poll_prepare () for s in self.slots]
            self._poll_thread = threading.Thread (target=self._poll)
            self._poll_thread.start ()

        ret = {s: [(i, val) for (i, val) in enumerate (self.slots[s].poll_cache)] for s in self.slots}
        self._poll_lock.release ()

        return ret

    def unsubscribe (self, callback):
        self._poll_lock.acquire ()
        self.subs.remove (callback)

        if not self.subs:
            self._poll_term.set ()
            self._poll_thread.join ()
            self._poll_term.clear ()

        self._poll_lock.release ()

