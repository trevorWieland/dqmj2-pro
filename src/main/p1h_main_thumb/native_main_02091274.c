#include "context.h"

/* Length of the first dotted segment. */
s32 native_main_02091274(const s8 *text)
{
    const s8 *start = text;

    while (*text != '.' && *text != 0)
        text++;
    return (s32)(text - start);
}
