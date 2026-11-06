#include "context.h"
void native_main_02093824(Rc4View *context,u8 *data,s32 length)
{
    s32 index;
    u8 x=context->x,y=context->y;
    u8 *state=context->state;
    u8 first,second;
    for(index=0;index<length;index++){
        first=state[++x];
        second=state[y+=first];
        state[x]=second;
        state[y]=first;
        data[index]^=state[(u8)(first+second)];
    }
    context->x=x;
    context->y=y;
}
