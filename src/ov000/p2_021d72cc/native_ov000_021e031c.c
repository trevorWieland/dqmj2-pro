#include "context.h"

/* Confirm both parameter blocks onto the actor, then store the value the pair
   resolves to as the first word of the 0x200 block. Reports success. */
s32 native_ov000_021e031c(Actor *actor, ParameterBlock *first, ParameterBlock *second)
{
    actor->field_1e8 = *first;
    actor->field_1f4 = *second;
    actor->field_200.word_0 = native_fn_0200285c(first, second);
    return 1;
}
