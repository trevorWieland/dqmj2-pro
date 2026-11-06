#include "context.h"
void native_main_02058c78(Context *context, const Instruction *instruction)
{
    context->parameters[0] = (float)native_fn_ov000_021e71f0() / 4096.0f;
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
