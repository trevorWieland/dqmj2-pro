#include "context.h"
void native_main_020937dc(Rc4View *context,u8 *key,s32 length)
{
    s32 index;
    u8 *state;
    u8 j,cursor,value;
    context->x=0;
    context->y=0;
    state=context->state;
    for(index=0;index<256;index++)state[index]=(u8)index;
    j=cursor=0;
    for(index=0;index<256;index++){
        value=state[index];
        j=(u8)(j+(value+key[cursor]));
        state[index]=state[j];
        state[j]=value;
        if(++cursor>=length)cursor=0;
    }
}
