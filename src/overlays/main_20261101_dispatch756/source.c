#include "context.h"
void native_main_0202f820(NNSG3dRS *rs) {
    do {
        u32 command;
        rs->flag &= ~0x40U;
        command = *rs->c;
        native_data_020dd790[command & 0x1FU](rs,command & 0xE0U);
    } while ((rs->flag & 0x20U) == 0);
}
