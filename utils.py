class Register:
    def __init__(self, value=0, bits_size=32):
        self.value = value
        self.bits_size = bits_size

    def get_lsb(self, bits):
        return self.value & (2**bits-1)

    def mov_lsb(self, bits, value):
        self.value = self.value ^ self.get_lsb(bits) | value

    def get_value(self):
        return self.value

    def mov(self, other):
        match other:
            case Register():
                self.value = other.value
            case int():
                self.value = other

    def rol(self, bits):
        mask = (2**self.bits_size - 1) ^ (2**(self.bits_size - bits) - 1)
        lsb = self.value & mask
        lsb >>= self.bits_size - bits
        self.value &= ~mask
        self.value <<= bits 
        self.value += lsb

    def ror(self, bits):
        mask = 2**bits - 1
        msb = self.value & mask
        msb <<= self.bits_size - bits
        self.value >>= bits
        self.value += msb

    def add(self, other):
        self.value = self.__add__(other)

    def inc(self):
        self.add(1)

    def add_lsb(self, bits, value):
        self.mov_lsb(bits, self.get_lsb(bits) + value)

    def sub(self, other):
        self.value = self.__sub__(other)

    def dec(self):
        self.sub(1)

    def sub_lsb(self, bits, value):
        self.mov_lsb(bits, self.get_lsb(bits) - value)

    def __str__(self):
        return bin(self.value)[2:].zfill(self.bits_size)

    def __add__(self, other):
        match other:
            case Register():
                return self.value + other.value
            case int():
                return self.value + other

    def __sub__(self, other):
        match other:
            case Register():
                return self.value - other.value
            case int():
                return self.value - other
