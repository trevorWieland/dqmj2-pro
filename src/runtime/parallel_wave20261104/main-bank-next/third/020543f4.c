#include "context.h"
void native_main_020543f4(Context *context, const Instruction *instruction)
{
    native_fn_02008140(0x40000000);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 1;
}
