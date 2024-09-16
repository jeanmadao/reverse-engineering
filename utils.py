class Register:
    def __init__(self, value=0, bits_size=32):
        self.value = value
        self.bits_size = bits_size

    @staticmethod
    def extract_value(other):
        match other:
            case Register():
                return other.value
            case int():
                return other


    def get_value(self):
        return self.value

    def mov(self, value):
        self.value = self.extract_value(value)

    def rol(self, rotation_bits):
        mask = (2**self.bits_size - 1) ^ (2**(self.bits_size - rotation_bits) - 1)
        lsb = self.value & mask
        lsb >>= self.bits_size - rotation_bits
        self.value &= ~mask
        self.value <<= rotation_bits
        self.value += lsb

    def ror(self, rotation_bits):
        mask = 2**rotation_bits - 1
        msb = self.value & mask
        msb <<= self.bits_size - rotation_bits
        self.value >>= rotation_bits
        self.value += msb

    def add(self, value):
        self.value = self.__add__(value)

    def inc(self):
        self.add(1)

    def sub(self, value):
        self.value = self.__sub__(value)

    def dec(self):
        self.sub(1)

    def get_sub(self, bits, offset_bit):
        return (self.value & ((2**bits - 1) << offset_bit)) >> offset_bit

    def reset_sub(self, bits, offset_bit):
        self.value ^= self.value & ((2**bits-1) << offset_bit)

    def mov_sub(self, bits, offset_bit, value):
        self.reset_sub(bits, offset_bit)
        self.value |= self.extract_value(value) << offset_bit

    def add_sub(self, bits, offset_bit, value):
        result = (self.get_sub(bits, offset_bit) + self.extract_value(value)) % (2**bits)
        self.mov_sub(bits, offset_bit, result)

    def sub_sub(self, bits, offset_bit, value):
        result = (self.get_sub(bits, offset_bit) - self.extract_value(value)) % (2**bits)
        self.mov_sub(bits, offset_bit, result)

    def __add__(self, value):
        return self.value + self.extract_value(value) % 2**self.bits_size

    def __sub__(self, value):
        return self.value - self.extract_value(value) % 2**self.bits_size

    def __str__(self):
        return bin(self.value)[2:].zfill(self.bits_size)
