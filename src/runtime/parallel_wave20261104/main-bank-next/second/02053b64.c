#include "context.h"
void native_main_02053b64(Context *context, const Instruction *instruction)
{
    native_fn_0205c338((u32)context->parameters[0]);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
