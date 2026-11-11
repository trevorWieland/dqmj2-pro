#include "context.h"

/* Count how many trailing zero halfwords the array has. */
u32 native_main_02093874(const u16 *array, u32 count)
{
    while (count != 0 && array[count - 1] == 0)
        count--;
    return count;
}
