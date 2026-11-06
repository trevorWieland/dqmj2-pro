#include "context.h"
void native_main_02058824(Context *context, const Instruction *instruction)
{
    native_fn_ov000_02209670();
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
