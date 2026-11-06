#include "context.h"
void native_main_0205857c(Context *context, const Instruction *instruction)
{
    signed char mode = (int)context->parameters[0];
    if (mode == -1) {
        u8 bank = context->bank;
        int value = native_fn_0203d0b4(63);
        if (bank == (value & 15))
            mode = 0;
        else if (bank == ((value >> 4) & 15))
            mode = 1;
        else
            mode = 0;
    }
    native_fn_ov000_022092c8(mode);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
