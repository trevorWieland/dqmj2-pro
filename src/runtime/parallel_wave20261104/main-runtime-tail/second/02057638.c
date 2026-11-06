#include "context.h"
void native_main_02057638(Context *context, const Instruction *instruction)
{
    native_fn_0205bf7c((u32)context->parameters[0]);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
