#include "context.h"
void native_main_020588ac(Context *context, const Instruction *instruction)
{
    native_fn_ov000_02209554();
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
