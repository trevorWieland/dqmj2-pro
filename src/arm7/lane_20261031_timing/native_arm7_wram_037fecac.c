#include "native_lane_sdk_types.h"
u16 native_arm7_wram_037fecac(int timer, int pitch)
{
    int octave = 0;
    int pitch_normalized = -pitch;

    while (pitch_normalized < 0)
    {
        octave--;
        pitch_normalized += 768;
    }

    while (pitch_normalized >= 768)
    {
        octave++;
        pitch_normalized -= 768;
    }

    u64 result = native_host_arm7_arm_037fedcc(pitch_normalized);

    result += 0x10000;
    result *= timer;

    int shift = octave - 16;

    if (shift <= 0)
    {
        shift = -shift;
        result >>= shift;
    }
    else if (shift < 32)
    {
        
        u64 tmp = result & ~0uLL << (32 - shift);
        if (tmp != 0)
            return 0xFFFF;
        result <<= shift;
    }
    else
    {
        return 0xFFFF;
    }

    if (result < 0x10)
        result = 0x10;
    else if (result > 0xFFFF)
        result = 0xFFFF;

    return (u16)result;
}
