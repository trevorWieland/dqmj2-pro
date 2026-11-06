#include "context.h"
void native_main_02053b0c(Context *context, const Instruction *instruction)
{
    native_fn_0205c338((u32)context->parameters[0] * 30);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
