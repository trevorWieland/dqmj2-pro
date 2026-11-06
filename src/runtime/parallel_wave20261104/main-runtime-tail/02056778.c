#include "context.h"
void native_main_02056778(Context *context, const Instruction *instruction)
{
    native_fn_02064038(native_fn_02064000());
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
