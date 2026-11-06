#include "context.h"
void native_main_02051310(Context *context, const Instruction *instruction)
{
    short first = (int)context->parameters[0];
    short second = (int)context->parameters[1];
    TargetRecord *target = native_fn_ov000_0221220c(first,second);
    target->slot70[0] += TO_FIXED(context->parameters[2]);
    target->slot70[1] += TO_FIXED(context->parameters[3]);
    target->slot70[2] += TO_FIXED(context->parameters[4]);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
