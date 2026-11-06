#include "context.h"
u32 native_main_0205fbb4(int index,int enabled)
{
    u32 *words=native_fn_02063e38();
    u32 result=native_fn_0205fb90(index);
    if(enabled)words[index>>5]|=1U<<(index&31);
    else words[index>>5]&=~(1U<<(index&31));
    return result;
}
