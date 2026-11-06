#include "context.h"
void native_main_02051c38(Context *context, const Instruction *instruction)
{
    native_fn_020405cc((u32)context->parameters[0]);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
