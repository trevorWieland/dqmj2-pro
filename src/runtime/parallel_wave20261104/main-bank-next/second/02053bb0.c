#include "context.h"
void native_main_02053bb0(Context *context, const Instruction *instruction)
{
    u8 slot = (u32)context->parameters[0];
    WordSlots *state = native_fn_02063e80();
    state->slots[slot] = 0;
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
