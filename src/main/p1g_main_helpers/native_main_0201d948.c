#include "context.h"

/* Signed-character search: return the first matching position, or the
   terminator position when searching for NUL, or NULL.  The loop is written as
   a guarded do-while because the measured body tests the first character
   before entering and again at the bottom. */
s8 *native_main_0201d948(const s8 *string, u32 character)
{
    s8 current = *string++;
    s8 c = (s8)character;

    if (current != 0) {
        do {
            if (current == c)
                return (s8 *)(string - 1);
            current = *string++;
        } while (current != 0);
    }
    if (c != 0)
        return 0;
    return (s8 *)(string - 1);
}
