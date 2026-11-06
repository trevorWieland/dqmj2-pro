#include "context.h"
s32 native_main_020d3dc0(s32 mode, u32 index)
{
    s32 result = -1;
    switch (mode) {
    case 1:
        if (index < 3) result = native_data_021d71fc[index].id0;
        break;
    case 2:
    case 3:
        if (index < 6) result = native_data_021d720e[index].id0;
        break;
    }
    return result;
}
