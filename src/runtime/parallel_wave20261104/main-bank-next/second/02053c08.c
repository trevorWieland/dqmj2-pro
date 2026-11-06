#include "context.h"
void native_main_02053c08(Context *context, const Instruction *instruction)
{
    u8 slot = (u32)context->parameters[0];
    WordSlots *state = native_fn_02063e80();
    context->parameters[0] = (float)state->slots[slot];
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
