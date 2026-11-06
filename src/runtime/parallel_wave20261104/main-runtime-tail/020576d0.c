#include "context.h"
void native_main_020576d0(Context *context, const Instruction *instruction)
{
    native_fn_0204071c(0);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
