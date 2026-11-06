#include "context.h"
s8 native_main_02060c60(u32 kindX, u32 kindY, u32 selectedX, u32 selectedY)
{
    s32 category = 1;
    s8 result;
    if (kindY == selectedY) category = 2;
    else if (kindY == 0) category = 0;
    result = category * 3;
    if (kindX != 0) {
        if (kindX == selectedX) result += 2;
        else result++;
    }
    return result;
}
