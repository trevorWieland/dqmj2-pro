#include "context.h"
void native_main_02058868(Context *context, const Instruction *instruction)
{
    native_fn_ov000_022096bc();
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
