#include "context.h"

/*
 * 0x020a3d9c (60 B, Thumb, p032/2.0-base)
 *
 * Drain the singly linked queue at 0x021d2300. Each node is released in two
 * 0x0209aa64 calls: the first with the node's size class 4 and its two payload
 * words, the second with the node itself and a zero selector. The named `node`
 * local is what keeps the loop-carried handle in r5, as the image does; a
 * fresh load per iteration puts it in r0 instead.
 *
 * Unknowns: the meaning of the 4-byte size class and of the second call's zero
 * selector; the producer that fills the queue.
 */

extern u32 native_fn_0209aa64();
extern u8 native_data_021d2300[];

void native_main_020a3d9c(void)
{
    u32 *node = *(u32 **)native_data_021d2300;

    if (node != 0) {
        do {
            *(u32 **)native_data_021d2300 = (u32 *)node[3];
            native_fn_0209aa64(4, node[1], node[2]);
            native_fn_0209aa64(4, node, 0);
            node = *(u32 **)native_data_021d2300;
        } while (node != 0);
    }
    ((u32 *)native_data_021d2300)[0] = 0;
    ((u32 *)native_data_021d2300)[1] = 0;
}
