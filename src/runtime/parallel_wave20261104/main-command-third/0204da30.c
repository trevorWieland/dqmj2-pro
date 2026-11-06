#include "context.h"
void native_main_0204da30(Context *context,const Instruction *instruction)
{
    int kind=(int)context->parameters[0];
    u8 first=(u32)context->parameters[1];
    u8 second=(u32)context->parameters[2];
    unsigned short third=(u32)context->parameters[3];
    if(kind==1) native_fn_02048034(native_fn_0205dc70(first,second,third),0);
    else if(kind==2) native_fn_02048034(native_fn_0205dc70(first,second,third),32);
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
