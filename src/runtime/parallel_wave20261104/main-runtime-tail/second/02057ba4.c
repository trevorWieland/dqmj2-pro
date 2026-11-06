#include "context.h"
void native_main_02057ba4(Context *context, const Instruction *instruction)
{
    native_fn_ov000_02218c24((u32)context->parameters[0]);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
