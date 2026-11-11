#include "context.h"

/* Skip one character of a packed string: a 0xc0 lead byte consumes one extra
   byte, other bytes advance by their own value. */
u8 *native_main_0208e620(u8 *text)
{
    u8 current = *text++;

    if (current == 0)
        return text;
    for (;;) {
        if ((current & 0xc0) == 0xc0)
            return text + 1;
        text += current;
        current = *text++;
        if (current == 0)
            return text;
    }
}
