Control Crevis Modbus I/O Adapters using Python
===============================================

This is a Python module to control Crevis Modbus I/O adapters, written
by [Tobias Waldekranz](https://github.com/wkz).

To use it:

```python
import crevisio

io = crevisio.adapter('198.18.122.10')

# Show some info about the adapter
print repr(io)

# Enable module 0, output pin 4
io[0][4] = True
```

For a more complete example, see [cio](cio).
