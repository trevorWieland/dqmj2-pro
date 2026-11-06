#include "context.h"
void native_main_02051dfc(Context *context, const Instruction *instruction)
{
    if (native_fn_02082458())
        context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 1;
}
