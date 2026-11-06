#include "dependency000.h"

void native_utility_child_arm9_main_0200f8dc (void)
{
    PXIFifoMessage fifomsg;
    PXIFifoStatus ret_code;
    PXIFifoTag tag;
    while (1) {
        ret_code = PXIi_GetFromFifo(&fifomsg.raw);
        if (ret_code == PXI_FIFO_FAIL_RECV_EMPTY)
            break;
        if (ret_code == PXI_FIFO_FAIL_RECV_ERR)
            continue;
        tag = (PXIFifoTag)fifomsg.e.tag;
        if (tag) {
            if (native_utility_child_arm9_data_0202cbcc[tag]) {
                (native_utility_child_arm9_data_0202cbcc[tag])(tag, fifomsg.e.data, (BOOL)fifomsg.e.err);
            } else {
                if (fifomsg.e.err) {
                } else {
                    fifomsg.e.err = 1 ;
                    (void)PXIi_SetToFifo(fifomsg.raw);
                }
            }
        } else {
        }
    }
}
