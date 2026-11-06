#include "context.h"
int native_main_0208eb34(s32 maximum)
{
    CommandPacket *packets;
    u32 packetBytes;
    void **messages;
    u32 messageBytes;
    messageBytes=((u32)maximum*sizeof(void *)+3)&~3;
    packetBytes=((u32)maximum*sizeof(CommandPacket)+3)&~3;
    messages=native_data_020de7cc->allocate18(packetBytes+messageBytes);
    if(!messages)return -1;
    native_fn_02006dfc(&native_data_021d1584,messages,maximum);
    packets=(CommandPacket *)((u32)messages+messageBytes);
    while(maximum>0){native_fn_0208ebfc(&packets->h);++packets;--maximum;}
    native_data_021d1580.array0=messages;
    return 0;
}
