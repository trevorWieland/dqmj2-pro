#include "context.h"
void native_main_02050fbc(Context *context, const Instruction *instruction)
{
    int first = (int)context->parameters[0];
    int second = (int)context->parameters[1];
    NativeVec3 a = {TO_FIXED(context->parameters[2]),TO_FIXED(context->parameters[3]),TO_FIXED(context->parameters[4])};
    int last = TO_FIXED(context->parameters[5]);
    native_fn_ov000_022122dc(first,second,&a,last);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
