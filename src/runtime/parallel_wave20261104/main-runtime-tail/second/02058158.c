#include "context.h"
void native_main_02058158(Context *context, const Instruction *instruction)
{
    context->parameters[0] = (float)(u8)native_fn_020d3fd0();
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
