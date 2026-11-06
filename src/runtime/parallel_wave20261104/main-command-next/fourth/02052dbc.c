#include "context.h"
void native_main_02052dbc(Context *context, const Instruction *instruction)
{
    int previous = native_fn_020629e0();
    int first = native_fn_02062aa0();
    int next_first;
    previous = previous - first - native_fn_02062ad0();
    next_first = native_fn_02062aa0();
    context->parameters[0] = (float)(100 - next_first - native_fn_02062ad0() - previous);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
