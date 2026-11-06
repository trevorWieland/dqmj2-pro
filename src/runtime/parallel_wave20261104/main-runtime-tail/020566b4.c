#include "context.h"
void native_main_020566b4(Context *context, const Instruction *instruction)
{
    int first = (int)context->parameters[0];
    int second = (int)context->parameters[1];
    native_fn_ov000_021f4110(first, (u8)second);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
