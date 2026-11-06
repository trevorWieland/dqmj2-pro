#include "context000.h"

void native_host_arm7_wram_038053d0(void)
{
    native_host_arm7_data_0380b258.status = MIC_STATUS_READY;
    for (int i = 0; i < 16 ; i++) {
        native_host_arm7_mic_words_0380b258[i] = 0;
    }
    (*( REGType16v *) (0x04000000 + 0x10e)) &= ~0x0080 ;
}
