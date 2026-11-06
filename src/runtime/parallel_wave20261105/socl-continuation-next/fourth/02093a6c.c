#include "context.h"
s32 native_main_02093a6c(u16 *left,u16 *right,s32 digits)
{
    s32 index;
    for(index=digits-1;index>=0;index--){
        if(left[index]>right[index])return 1;
        if(left[index]<right[index])return -1;
    }
    return 0;
}
