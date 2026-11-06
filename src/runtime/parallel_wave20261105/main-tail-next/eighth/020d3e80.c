#include "context.h"
u32 native_main_020d3e80(s32 mode, u32 index)
{
    u32 result = 0;
    switch (mode) {
    case 1:
        if (index < 3) result = native_data_021d7200[index].value0;
        break;
    case 2:
    case 3:
        if (index < 6) result = native_data_021d7212[index].value0;
        break;
    }
    return result;
}
