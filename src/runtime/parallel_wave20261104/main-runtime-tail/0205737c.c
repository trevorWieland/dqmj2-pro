#include "context.h"
void native_main_0205737c(Context *context, const Instruction *instruction)
{
    if (native_fn_ov000_021e9aa0())
        context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 1;
}
