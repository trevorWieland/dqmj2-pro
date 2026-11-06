#include "native_sdk_connected_types.h"
void native_arm7_wram_03800310(int player,const void *sequence,u32 offset,void *bank)
{
    native_host_arm7_arm_038000b4(player,sequence,offset,bank);
    native_host_arm7_data_03808420[player].flags |= 2;
}
