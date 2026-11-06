#include "context.h"
void native_main_0208d178(u32 first,TransportHeader *packet,u32 bytes)
{
    if(native_fn_0208bbac(packet,bytes,(const void *)first,6)!=0)return;
    bytes-=(packet->dataOffset12&0xf0)/4;
    switch(packet->flags13&0x17){
    case 2:
        if(packet->flags13&0x28)return;
        native_fn_0208cdd0(first,(u32)packet,bytes);
        break;
    case 18:
        if(packet->flags13&0x28)return;
        native_fn_0208ce58(first,(u32)packet,bytes);
        break;
    case 16:
    case 17:
        native_fn_0208cef0(first,(u32)packet,bytes);
        break;
    case 1:
        native_fn_0208d0e0(first,(u32)packet,bytes);
        break;
    default:
        if(packet->flags13&4)native_fn_0208d154(first,(u32)packet);
        else native_fn_0208cc24(first,(u32)packet,bytes,0);
    }
}
