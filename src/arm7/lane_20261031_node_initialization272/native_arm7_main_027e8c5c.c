#include "native_node_types.h"
void native_arm7_main_027e8c5c(u32 address, u32 id)
{
    NativeNode *node = (NativeNode *)address;
    node->previous = 0xffffffffU;
    node->next = 0xffffffffU;
    node->count = 0;
    node->id = (u16)id;
}
