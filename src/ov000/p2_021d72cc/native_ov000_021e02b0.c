#include "context.h"

/* Confirm the three parameter blocks onto the actor, clear the install
   selection, and report success. */
s32 native_ov000_021e02b0(Actor *actor, ParameterBlock *first, ParameterBlock *second,
                          ParameterBlock *third)
{
    actor->field_1f4 = *first;
    actor->field_1e8 = *second;
    actor->field_200 = *third;
    actor->field_20c = 0;
    return 1;
}
