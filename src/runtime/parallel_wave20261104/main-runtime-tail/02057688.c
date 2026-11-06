#include "context.h"
void native_main_02057688(Context *context, const Instruction *instruction)
{
    native_fn_0204071c(1);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
