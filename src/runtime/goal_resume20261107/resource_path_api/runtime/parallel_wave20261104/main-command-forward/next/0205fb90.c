#include "../../../../resource_path_api.h"
#include "context.h"
u32 native_main_0205fb90(int index)
{
    u32 *words=native_fn_02063e38();
    return (words[index>>5]>>(index&31))&1;
}
