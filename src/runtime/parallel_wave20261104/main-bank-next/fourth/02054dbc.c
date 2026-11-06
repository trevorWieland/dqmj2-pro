#include "context.h"
void native_main_02054dbc(Context *context, const Instruction *instruction)
{
    signed char value = (int)context->parameters[0];
    context->records[context->bank].position += instruction->advance;
    native_fn_ov007_021d9760(value);
    context->records[context->bank].status = 0;
}
