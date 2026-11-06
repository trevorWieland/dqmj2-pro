#include "context000.h"

void native_host_arm7_wram_03805784(SPIEntry *entry)
{
    switch (entry->process) {
    case 0x0040 : {
        OSIntrMode e = native_host_arm7_arm_037fdd00();
        if (!native_host_arm7_arm_03803b0c(SPI_DEVICE_TYPE_MIC)) {
            native_host_arm7_arm_037fdd14(e);
            native_host_arm7_arm_03803a48(entry->process, 0x0004 );
            return;
        }
        native_host_arm7_arm_03803b28(SPI_DEVICE_TYPE_MIC);
        native_host_arm7_arm_037fdd14(e);
    }
        if ((entry->arg[0] & 0x0001 ) == 0x0001 ) {
            u16 temp = native_host_arm7_arm_03805cd4();
            if (entry->arg[0] & 0x0002 ) {
                temp ^= 0x8000;
            }
            ((OSSystemWork *)(0x02000000 + 0x007ffc00)) ->mic_sampling_data = temp;
            ((OSSystemWork *)(0x02000000 + 0x007ffc00)) ->mic_last_address = (0x02000000 + 0x007fff94) ;
        } else {
            u16 temp = native_host_arm7_arm_03805b80();
            if (entry->arg[0] & 0x0002 ) {
                temp ^= 0x0080;
            }
            ((OSSystemWork *)(0x02000000 + 0x007ffc00)) ->mic_sampling_data = temp;
            ((OSSystemWork *)(0x02000000 + 0x007ffc00)) ->mic_last_address = (0x02000000 + 0x007fff94) ;
        }
        native_host_arm7_arm_03803a48((u16)(entry->process), 0x0000 );
        native_host_arm7_arm_03803b40(SPI_DEVICE_TYPE_MIC);
        break;
    case 0x0041 :
        if (native_host_arm7_data_0380b258.status == MIC_STATUS_AUTO_START) {
            native_host_arm7_data_0380b258.temporary = 0;
            native_host_arm7_data_0380b258.temp16 = 0;
            OSIntrMode e = native_host_arm7_arm_037fdd00();
            native_host_arm7_arm_037fb8f0((1UL << 6) );
            native_host_arm7_arm_03805e08((1UL << 6) , native_host_arm7_arm_038059ac);
            native_host_arm7_arm_03805e30();
            (*( REGType16v *) (0x04000000 + 0x10c)) = native_host_arm7_data_0380b258.timerValue;
            (*( REGType16v *) (0x04000000 + 0x10e)) = (u16)(0x0080 | 0x0040 | native_host_arm7_data_0380b258.timerPrescaler);
            native_host_arm7_arm_037fdd14(e);
            native_host_arm7_arm_03803a48(entry->process, 0x0000 );
            native_host_arm7_data_0380b258.status = MIC_STATUS_AUTO_SAMPLING;
        } else {
            native_host_arm7_arm_03803a48(entry->process, 0x0003 );
        }
        break;
    case 0x0042 :
        if (native_host_arm7_data_0380b258.status == MIC_STATUS_AUTO_END || native_host_arm7_data_0380b258.status == MIC_STATUS_END_WAIT) {
            (*( REGType16v *) (0x04000000 + 0x10e)) &= ~0x0080 ;
            OSIntrMode e = native_host_arm7_arm_037fdd00();
            native_host_arm7_arm_03805e08((1UL << 6) , ((void *)0) );
            native_host_arm7_arm_03805e90();
            native_host_arm7_arm_037fdd14(e);
            if (native_host_arm7_data_0380b258.status == MIC_STATUS_AUTO_END) {
                native_host_arm7_arm_03803a48(0x0042 , 0x0000 );
            } else {
                native_host_arm7_arm_03803a48(0x0051 , 0x0000 );
            }
            native_host_arm7_data_0380b258.status = MIC_STATUS_READY;
        } else {
            if (native_host_arm7_data_0380b258.status == MIC_STATUS_AUTO_END) {
                native_host_arm7_arm_03803a48(0x0042 , 0x0003 );
            } else {
                native_host_arm7_arm_03803a48(0x0051 , 0x0003 );
            }
        }
        break;
    }
}

#include "context001.h"
