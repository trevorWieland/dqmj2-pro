#include "context.h"
void native_main_02050c88(Context *context, const Instruction *instruction)
{
    int first = (int)context->parameters[0];
    int second = (int)context->parameters[1];
    int third = (int)context->parameters[2];
    if (!native_fn_ov000_0221221c(first,second,third))
        native_fn_ov000_022124e8(first,second,third);
    if (!native_fn_ov000_0221225c(first,second,third))
        native_fn_ov000_02212518(first,second,third);
    native_fn_ov000_0221229c(first,second,third);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
