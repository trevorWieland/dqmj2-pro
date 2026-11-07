#include "context000.h"

SPITpValidity native_host_arm7_wram_038044bc(u16 *data, s32 range, TPDetectAxis axis, u16 *density)
{
    s32 i, j, k;
    s32 temp[5 ];
    u16 command;
    SPITpValidity validity;
    ((void) 0) ;
    ((void) 0) ;
    if (axis == TP_DETECT_AXIS_X) {
        command = 0xD1 ;
        validity = SPI_TP_VALIDITY_INVALID_X;
    } else {
        command = 0x91 ;
        validity = SPI_TP_VALIDITY_INVALID_Y;
    }
    SPI_Wait();
    TP_SPIChangeMode(SPI_TRANSMODE_CONTINUOUS);
    SPI_SendWait(command);
    for (i = 0; i < 5 ; i++) {
        temp[i] = (SPI_DummyWaitReceive()) << 8;
        temp[i] |= SPI_SendWaitReceive(command);
        temp[i] = (temp[i] & 0x7FF8 ) >> 3 ;
    }
    TP_SPIChangeMode(SPI_TRANSMODE_1BYTE);
    native_host_arm7_arm_03804498();
    s32 maxRange = 0;
    for (i = 0; i < 5 - 1; i++) {
        for (j = i + 1; j < 5 ; j++) {
            s32 range = (((temp[i] - temp[j]) < 0) ? (-(temp[i] - temp[j])) : (temp[i] - temp[j])) ;
            if (range > maxRange) {
                maxRange = range;
            }
        }
    }
    *density = maxRange;
    for (i = 0; i < 5 - 2; i++) {
        for (j = i + 1; j < 5 - 1; j++) {
            if ((((temp[i] - temp[j]) < 0) ? (-(temp[i] - temp[j])) : (temp[i] - temp[j])) > range) {
                continue;
            }
            for (k = j + 1; k < 5 ; k++) {
                if ((((temp[i] - temp[k]) < 0) ? (-(temp[i] - temp[k])) : (temp[i] - temp[k])) <= range) {
                    *data = (u16)((((temp[i] << 1) + temp[j] + temp[k]) >> 2) & ~0x7);
                    return SPI_TP_VALIDITY_VALID;
                }
            }
        }
    }
    *data = ((temp[0] + temp[4]) >> 1) & ~0x7;
    return validity;
}
