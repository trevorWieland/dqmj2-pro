#include "context.h"

/* Confirm the two parameter blocks onto the actor and report success. */
s32 native_ov000_021e02f0(Actor *actor, ParameterBlock *first, ParameterBlock *second)
{
    actor->field_1f4 = *first;
    actor->field_1e8 = *second;
    return 1;
}
