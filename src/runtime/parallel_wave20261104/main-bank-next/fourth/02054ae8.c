#include "context.h"
void native_main_02054ae8(Context *context, const Instruction *instruction)
{
    native_fn_02063db8((int)context->parameters[0]);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
