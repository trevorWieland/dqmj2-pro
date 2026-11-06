#include "context000.h"

void native_host_arm7_wram_03805418(u32 data)
{
    if (data & 0x02000000 ) {
        for (int i = 0; i < 16 ; i++) {
            native_host_arm7_mic_words_0380b258[i] = 0;
        }
    }
    native_host_arm7_mic_words_0380b258[(data & 0x000f0000 ) >> 16 ] = (data & 0x0000ffff ) >> 0 ;
    if (data & 0x01000000 ) {
        u16 command = (native_host_arm7_data_0380b258.command[0] & 0xFF00) >> 8;
        u32 wu32;
        switch (command) {
        case 0x0040 :
            if (!native_host_arm7_arm_03803b7c(SPI_DEVICE_TYPE_MIC, command, 1, native_host_arm7_data_0380b258.command[0] & 0xFF)) {
                native_host_arm7_arm_03803a48(command, 0x0004 );
            }
            ((OSSystemWork *)(0x02000000 + 0x007ffc00)) ->mic_sampling_data = 0;
            ((OSSystemWork *)(0x02000000 + 0x007ffc00)) ->mic_last_address = (u32)((void *)0) ;
            break;
        case 0x0041 :
            if (native_host_arm7_data_0380b258.status != MIC_STATUS_READY) {
                native_host_arm7_arm_03803a48(command, 0x0003 );
                return;
            }
            native_host_arm7_data_0380b258.type = native_host_arm7_data_0380b258.command[0] & 0xFF;
            wu32 = (native_host_arm7_data_0380b258.command[1] << 16) | native_host_arm7_data_0380b258.command[2];
            if ((wu32 < 0x02000000 ) || (wu32 >= (0x02000000 + 0x00400000) )) {
                native_host_arm7_arm_03803a48(command, 0x0002 );
                return;
            }
            native_host_arm7_data_0380b258.buf = (void *)wu32;
            wu32 = (native_host_arm7_data_0380b258.command[3] << 16) | native_host_arm7_data_0380b258.command[4];
            if ((u32)native_host_arm7_data_0380b258.buf + wu32 > (0x02000000 + 0x00400000) ) {
                native_host_arm7_arm_03803a48(command, 0x0002 );
                return;
            }
            native_host_arm7_data_0380b258.size = wu32;
            wu32 = (native_host_arm7_data_0380b258.command[5] << 16) | native_host_arm7_data_0380b258.command[6];
            if (!native_host_arm7_arm_038056e0(wu32)) {
                native_host_arm7_arm_03803a48(command, 0x0002 );
                return;
            }
            native_host_arm7_data_0380b258.index = 0;
            native_host_arm7_data_0380b258.admode = native_host_arm7_data_0380b258.type & 0x0007 ;
            if (!native_host_arm7_arm_03803b7c(SPI_DEVICE_TYPE_MIC, (u32)command, 0)) {
                native_host_arm7_arm_03803a48(command, 0x0004 );
                return;
            }
            ((OSSystemWork *)(0x02000000 + 0x007ffc00)) ->mic_sampling_data = 0;
            ((OSSystemWork *)(0x02000000 + 0x007ffc00)) ->mic_last_address = (u32)((void *)0) ;
            native_host_arm7_data_0380b258.status = MIC_STATUS_AUTO_START;
            break;
        case 0x0042 :
            if (native_host_arm7_data_0380b258.status != MIC_STATUS_AUTO_SAMPLING) {
                native_host_arm7_arm_03803a48(command, 0x0003 );
                return;
            }
            if (!native_host_arm7_arm_03803b7c(SPI_DEVICE_TYPE_MIC, command, 0)) {
                native_host_arm7_arm_03803a48(command, 0x0004 );
                return;
            }
            native_host_arm7_data_0380b258.status = MIC_STATUS_AUTO_END;
            (*( REGType16v *) (0x04000000 + 0x10e)) &= ~0x0080 ;
            break;
        case 0x0043 :
            if (native_host_arm7_data_0380b258.status != MIC_STATUS_AUTO_SAMPLING) {
                native_host_arm7_arm_03803a48(command, 0x0003 );
                return;
            }
            wu32 = (native_host_arm7_data_0380b258.command[1] << 16) | native_host_arm7_data_0380b258.command[2];
            if (!native_host_arm7_arm_038056e0(wu32)) {
                native_host_arm7_arm_03803a48(command, 0x0002 );
                return;
            }
            OSIntrMode e = native_host_arm7_arm_037fdd00();
            (*( REGType16v *) (0x04000000 + 0x10e)) &= ~0x0080 ;
            (*( REGType16v *) (0x04000000 + 0x10c)) = native_host_arm7_data_0380b258.timerValue;
            (*( REGType16v *) (0x04000000 + 0x10e)) = (u16)(0x0080 | 0x0040 | native_host_arm7_data_0380b258.timerPrescaler);
            native_host_arm7_arm_037fdd14(e);
            native_host_arm7_arm_03803a48(command, 0x0000 );
            break;
        default:
            native_host_arm7_arm_03803a48(command, 0x0001 );
        }
    }
}

#include "context001.h"
