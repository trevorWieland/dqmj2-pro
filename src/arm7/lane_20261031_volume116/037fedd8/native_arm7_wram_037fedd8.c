#include "native_volume_types.h"
u16 native_arm7_wram_037fedd8(int value)
{
    if (value < SND_VOL_DB_MIN)
        value = SND_VOL_DB_MIN;
    else if (value > 0)
        value = 0;

    int result = SVC_GetVolumeTable(value + (-SND_VOL_DB_MIN));
    int div;

    if (value < -240)
        div = 3;
    else if (value < -120)
        div = 2;
    else if (value < -60)
        div = 1;
    else
        div = 0;

    return (u16)(result | (div << 8));
}
