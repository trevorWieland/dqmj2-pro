#include "context.h"

/* Record with the 16-bit fields at 0x34, 0x36, 0x38 and 0x3a. */
typedef struct {
    u8 pad[0x34];
    u16 mode;    /* +0x34 */
    u16 field36; /* +0x36 */
    u16 value;   /* +0x38 */
    u16 extra;   /* +0x3a */
} SceneRecord;

/* Start the live record in mode 1 with one 16-bit value. */
void native_main_020381d4(SceneRecord *volatile *slot, u16 value)
{
    if (*slot == 0)
        return;
    (*slot)->mode = 1;
    (*slot)->value = value;
}

