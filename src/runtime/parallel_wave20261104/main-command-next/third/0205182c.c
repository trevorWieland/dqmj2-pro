#include "context.h"
void native_main_0205182c(Context *context, const Instruction *instruction)
{
    int first = (int)context->parameters[0];
    int second = (int)context->parameters[1];
    NativeVec3 value = {TO_FIXED(context->parameters[2]),TO_FIXED(context->parameters[3]),TO_FIXED(context->parameters[4])};
    native_fn_ov000_02212720(first,second,value);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
