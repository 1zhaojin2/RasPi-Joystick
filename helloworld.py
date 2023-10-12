import pyopencl as cl
import numpy as np

def _l2M3N4O7R8S9T0_():
    return """
    kernel void d(global const int *x, global int *y) {
        unsigned int _aBcDeFgHiJkLmNoP_ = get_global_id(0);
        y[_aBcDeFgHiJkLmNoP_] = x[_aBcDeFgHiJkLmNoP_] - 1;
    }
    """

def _g3H4I5J6K7gWEa4L8M9N0O1_(_v6W7A1C3D4_, _t2U3V4W5X6Y7Z8A9B0_):
    _p01R2S3GS7GE903GYSg979GEGAW524U5V6W7X8_ = cl.Buffer(_v6W7A1C3D4_, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=_t2U3V4W5X6Y7Z8A9B0_)
    _q9R0S1T2U3V4W5X6Y7_ = np.empty_like(_t2U3V4W5X6Y7Z8A9B0_)
    _r8S9T0U1V2W3X4Y5Z6_ = cl.Buffer(_v6W7A1C3D4_, cl.mem_flags.WRITE_ONLY, _q9R0S1T2U3V4W5X6Y7_.nbytes)
    return _p01R2S3GS7GE903GYSg979GEGAW524U5V6W7X8_, _q9R0S1T2U3V4W5X6Y7_, _r8S9T0U1V2W3X4Y5Z6_

def _u9V0W1X2Y3Z4A5B7_():
    _d8_ = cl.get_platforms()[0]
    _m7N8O9P0Q1R2S3T4U5_ = _d8_.get_devices(cl.device_type.GPU)
    _v6W7A1C3D4_ = cl.Context(_m7N8O9P0Q1R2S3T4U5_)
    _e5F6G7H8I9J0K1L2M3_ = cl.CommandQueue(_v6W7A1C3D4_)
    return _v6W7A1C3D4_, _e5F6G7H8I9J0K1L2M3_

def _s7T8U9fwV0W1GZ4A5_(_v6W7A1C3D4_, _s6T7U8V9W0X9S2Z2A3B4_):
    return cl.Program(_v6W7A1C3D4_, _s6T7U8V9W0X9S2Z2A3B4_).build()

def _t6U73B4_(_e5F6G7H8I9J0K1L2M3_, _w5X6Y7Z8A9B0C1D2E3_, _p01R2S3GS7GE903GYSg979GEGAW524U5V6W7X8_, _r8S9T0U1V2W3X4Y5Z6_, _q9R0S1T2U3V4W5X6Y7_):
    _w5X6Y7Z8A9B0C1D2E3_.d(_e5F6G7H8I9J0K1L2M3_, _q9R0S1T2U3V4W5X6Y7_.shape, None, _p01R2S3GS7GE903GYSg979GEGAW524U5V6W7X8_, _r8S9T0U1V2W3X4Y5Z6_)
    cl.enqueue_copy(_e5F6G7H8I9J0K1L2M3_, _q9R0S1T2U3V4W5X6Y7_, _r8S9T0U1V2W3X4Y5Z6_)

def _f4G5H6I7J8K9L0M1N2_():
    return np.array([1, 2, 3, 3, 4, 8, 5, 4, 6, 3, 7], dtype=np.int32)

def _a1B2f2Bc3D4e5F6g7H8_():
    _a1r2c3fn2eF8gg2y = {
        'A': 'H', 'B': 'e', 'C': 'l', 'D': 'o', 'E': 'W', 'F': 'r', 'G': 'd', 'H': ' '
    }
    _r21CsfgdaY3sdgdf_ = ['0x41', '0x42', '0x43', '0x44', '0x45', '0x46', '0x47', '0x48']
    _gEev6esCEggr7SE6_ = [chr(int(_25v1SV53svY42_, 16)) for _25v1SV53svY42_ in _r21CsfgdaY3sdgdf_]
    return ''.join(_a1r2c3fn2eF8gg2y[_as3t3FD6evT3s3VHs_] for _as3t3FD6evT3s3VHs_ in _gEev6esCEggr7SE6_)

def main():
    _z4A5B6C7D89F0G1H2_ = _a1B2f2Bc3D4e5F6g7H8_()
    _s6T7U8V9W0X9S2Z2A3B4_ = _l2M3N4O7R8S9T0_()
    _v6W7A1C3D4_, _e5F6G7H8I9J0K1L2M3_ = _u9V0W1X2Y3Z4A5B7_()
    _t2U3V4W5X6Y7Z8A9B0_ = _f4G5H6I7J8K9L0M1N2_()
    _p01R2S3GS7GE903GYSg979GEGAW524U5V6W7X8_, _q9R0S1T2U3V4W5X6Y7_, _r8S9T0U1V2W3X4Y5Z6_ = _g3H4I5J6K7gWEa4L8M9N0O1_(_v6W7A1C3D4_, _t2U3V4W5X6Y7Z8A9B0_)
    _w5X6Y7Z8A9B0C1D2E3_ = _s7T8U9fwV0W1GZ4A5_(_v6W7A1C3D4_, _s6T7U8V9W0X9S2Z2A3B4_)
    _t6U73B4_(_e5F6G7H8I9J0K1L2M3_, _w5X6Y7Z8A9B0C1D2E3_, _p01R2S3GS7GE903GYSg979GEGAW524U5V6W7X8_, _r8S9T0U1V2W3X4Y5Z6_, _q9R0S1T2U3V4W5X6Y7_)
    print(''.join([_z4A5B6C7D89F0G1H2_[_aBcDeFgHiJkLmNoP_] for _aBcDeFgHiJkLmNoP_ in _q9R0S1T2U3V4W5X6Y7_]))

if __name__ == "__main__":
    main()