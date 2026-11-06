#include "context.h"
void native_main_02052190(Context *context, const Instruction *instruction)
{
    u8 first = (u32)context->parameters[0];
    NativeVec3 value = {TO_FIXED(context->parameters[1]),TO_FIXED(context->parameters[2]),TO_FIXED(context->parameters[3])};
    u8 last = (int)context->parameters[4];
    native_fn_ov000_021e5c88(first,0,&value,last);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
