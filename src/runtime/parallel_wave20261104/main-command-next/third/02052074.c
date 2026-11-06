#include "context.h"
void native_main_02052074(Context *context, const Instruction *instruction)
{
    native_fn_ov000_02212e1c((int)context->parameters[0]);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
