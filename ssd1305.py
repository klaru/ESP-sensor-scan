# MicroPython SSD1305 OLED driver, I2C interface

from micropython import const

try:
    import framebuf
except ImportError:
    import adafruit_framebuf as framebuf

# register definitions
MONOLSB = const (0x0)

SET_CONTRAST = const(0x81)
SET_ENTIRE_ON = const(0xA4)
SET_NORM_INV = const(0xA6)
SET_DISP = const(0xAE)
SET_MEM_ADDR = const(0x20)
SET_COL_ADDR = const(0x21)
SET_PAGE_ADDR = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_LUT = const(0x91)
SET_SEG_REMAP = const(0xA0)
SET_MUX_RATIO = const(0xA8)
SET_MASTER_CONFIG = const(0xAD)
SET_COM_OUT_DIR = const(0xC0)
SET_COMSCAN_DEC = const(0xC8)
SET_DISP_OFFSET = const(0xD3)
SET_COM_PIN_CFG = const(0xDA)
SET_DISP_CLK_DIV = const(0xD5)
SET_AREA_COLOR = const(0xD8)
SET_PRECHARGE = const(0xD9)
SET_VCOM_DESEL = const(0xDB)
SET_CHARGE_PUMP = const(0x8D)

class SSD1305(framebuf.FrameBuffer):
    def __init__(self, buffer, width, height, *, external_vcc):
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height // 8
        self._column_offset = 0
        if self.height == 32:
            self._column_offset = 4  # hardcoded for now...
        super().__init__(buffer, width, height, MONOLSB)
        self.init_display()

    def init_display(self):
        for cmd in (
            SET_DISP | 0x00,  # off
            # timing and driving scheme
            SET_DISP_CLK_DIV,
            0x80,  # SET_DISP_CLK_DIV
            SET_SEG_REMAP | 0x01,  # column addr 127 mapped to SEG0 SET_SEG_REMAP
            SET_MUX_RATIO,
            self.height - 1,  # SET_MUX_RATIO
            SET_DISP_OFFSET,
            0x00,  # SET_DISP_OFFSET
            SET_MASTER_CONFIG,
            0x8E,  # Set Master Configuration
            SET_AREA_COLOR,
            0x05,  # Set Area Color Mode On/Off & Low Power Display Mode
            SET_MEM_ADDR,
            0x00,  # horizontal SET_MEM_ADDR ADD
            SET_DISP_START_LINE | 0x00,
            0x2E,  # SET_DISP_START_LINE ADD
            SET_COMSCAN_DEC,  # Set COM Output Scan Direction 64 to 1
            SET_COM_PIN_CFG,
            0x12,  # SET_COM_PIN_CFG
            SET_LUT,
            0x3F,
            0x3F,
            0x3F,
            0x3F,  # Current drive pulse width of BANK0, Color A, B, C
            SET_CONTRAST,
            0xFF,  # maximum SET_CONTRAST to maximum
            SET_PRECHARGE,
            0xD2,  # SET_PRECHARGE orig: 0xd9, 0x22 if self.external_vcc else 0xf1,
            SET_VCOM_DESEL,
            0x34,  # SET_VCOM_DESEL 0xdb, 0x30, $ 0.83* Vcc
            SET_NORM_INV,  # not inverted SET_NORM_INV
            SET_ENTIRE_ON,  # output follows RAM contents  SET_ENTIRE_ON
            SET_CHARGE_PUMP,
            0x10 if self.external_vcc else 0x14,  # SET_CHARGE_PUMP
            SET_DISP | 0x01,
        ):  # //--turn on oled panel
            self.write_cmd(cmd)
        self.fill(0)
        self.show()

    def poweroff(self):
        self.write_cmd(SET_DISP | 0x00)

    def poweron(self):
        self.write_cmd(SET_DISP | 0x01)

    def contrast(self, contrast):
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        self.write_cmd(SET_NORM_INV | (invert & 1))

    def show(self):
        xpos0 = 0
        xpos1 = self.width - 1
        if self.width == 64:
            # displays with width of 64 pixels are shifted by 32
            xpos0 += 32
            xpos1 += 32
        self.write_cmd(SET_COL_ADDR)
        self.write_cmd(xpos0 + self._column_offset)
        self.write_cmd(xpos1 + self._column_offset)
        self.write_cmd(SET_PAGE_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.pages - 1)
        self.write_framebuf()


class SSD1305_I2C(SSD1305):
    def __init__(self, width, height, i2c, *, addr=0x3C, external_vcc=False):
        self.i2c = i2c
        self.addr = addr
        self.temp = bytearray(2)
        self.buffer = bytearray(((height // 8)* width) +1)
        self.buffer[0] = 0x40  # Co=0, D/C#=1
        super().__init__(
            memoryview(self.buffer)[1:],
            width, height, external_vcc=external_vcc)

    def write_cmd(self, cmd):
        self.temp[0] = 0x80  # Co=1, D/C#=0
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)

    def write_framebuf(self):
        self.i2c.writeto(self.addr, self.buffer)
