#include "context.h"
void native_main_0205908c(Context *context, const Instruction *instruction)
{
    native_fn_020d3ee0();
    native_fn_020d38f0(0);
    native_fn_020d37f0();
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
