Control Crevis Modbus I/O Adapters using Python
===============================================

Python module that lets you control discrete I/O pins on Modbus
adapters from Crevis. E.g. the [NA9189](http://beijerelectronics.co.in/en/Products/Distributed___IO/network-adapter-modules/Network___adapter___modules/MODBUS-TCP___NA9189.html).

The module uses the following, possibly very idiosyncratic,
terminology:

| Term    | Meaning                                                                       |
|---------|-------------------------------------------------------------------------------|
| Adapter | Represents an entire I/O device.                                              |
| Module  | Each adapter has 0 or more modules connected to it.                           |
| Slot    | Each module is referenced by its slot number, i.e. distance from the adapter. |
| Pin     | The pin number on a module, a slot:pin tuple identifies a specific pin.       |

To use it:

```python
import crevisio

# Connect to the adapter
io = crevisio.adapter('198.18.122.10')

# Show some info about the adapter
print repr(io)

# Enable module 0, output pin 4
io[0][4] = True
```

`cio`
=====

A commandline interface to `crevisio`.

In a typical setup, you often contact the same I/O, and have fixed
equipment connected to the I/O pins. For that reason, `cio` can read
the default address from a configuration file, avoiding the need to
specify it at every invocation. The configuration file can also be
used to reference individual pins using aliases.

A simple example may look like this:

```yaml
address: 192.168.0.100

aliases:
  - name: coffee-maker
    slot: 0
    pin:  1
  - name: nuke
    slot: 0
    pin:  4
  - name: door-bell
    slot: 0
    pin:  5
```

If you install the
[argcomplete](https://github.com/kislyuk/argcomplete) package, `cio`
will be able to autocomplete pin aliases from your configuration file.

`cio` will load the first file in any of the following paths:
- `~/.cio.yaml`
- `~/.config/cio.yaml`
- `/etc/cio.yaml`

That means that if your system administrator has setup `cio` already,
you do not have to do anything. But if you would like to use a
different address, or different aliases, you can override the system
default settings.

See `cio --help` for more information on command usage.
