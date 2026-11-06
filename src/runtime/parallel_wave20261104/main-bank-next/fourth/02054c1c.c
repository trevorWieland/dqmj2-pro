#include "context.h"
void native_main_02054c1c(Context *context, const Instruction *instruction)
{
    int object = (int)context->parameters[0];
    int slot = (int)context->parameters[1];
    u8 data[4] = {0, 0, 0, 0};
    u32 handle;
    switch (slot) {
    case 0: data[0] = 100; break;
    case 1: data[1] = 100; break;
    case 2: data[2] = 100; break;
    case 3: data[3] = 100; break;
    }
    handle = native_fn_020725e8(object);
    native_fn_020c1fdc(handle, data);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
