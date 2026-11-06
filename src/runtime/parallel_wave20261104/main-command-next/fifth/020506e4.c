#include "context.h"
void native_main_020506e4(Context *context, const Instruction *instruction)
{
    int index;
    int other;
    int value = (int)context->parameters[0];
    other = (int)context->parameters[1];
    if (value < 0) value = 0;
    else if (value > 127) value = 127;
    index = 0;
    do {
        if (native_fn_0205f2d8(index)) native_fn_0205e814(index,value,other);
        index++;
    } while (index < 16);
    index = 0;
    do {
        if (native_fn_0205f45c(index)) native_fn_0205f7e0(index,value,other);
        index++;
    } while (index < 4);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
