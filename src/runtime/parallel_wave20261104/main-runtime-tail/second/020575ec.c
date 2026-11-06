#include "context.h"
void native_main_020575ec(Context *context, const Instruction *instruction)
{
    context->parameters[0] = (float)native_fn_0205bf9c();
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
