#include "context.h"

/* Run the actor's completion callback when one is installed. Returns 0 when no
   callback exists, 1 once it has run. */
s32 native_ov000_021e0008(Actor *actor, s32 value)
{
    void (*callback)(s32) = (void (*)(s32))actor->field_264;

    if (callback == 0)
        return 0;
    callback(value);
    return 1;
}
