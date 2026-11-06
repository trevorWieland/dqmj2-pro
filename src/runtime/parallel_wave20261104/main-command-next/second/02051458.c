#include "context.h"
void native_main_02051458(Context *context, const Instruction *instruction)
{
    short first = (int)context->parameters[0];
    short second = (int)context->parameters[1];
    TargetRecord *target = native_fn_ov000_0221220c(first,second);
    target->slot88[1] = TO_FIXED(context->parameters[2]);
    target->state09 = 1;
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
