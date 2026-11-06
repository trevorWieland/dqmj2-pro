#include "context.h"
void native_main_02054064(Context *context, const Instruction *instruction)
{
    int first = (int)context->parameters[0];
    int second = (int)context->parameters[1];
    int word = (int)((u32)second << 12);
    int value = (int)(second > 0 ? 0.5f + (float)word : (float)word - 0.5f);
    native_fn_ov000_021e8e6c(first, value);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
