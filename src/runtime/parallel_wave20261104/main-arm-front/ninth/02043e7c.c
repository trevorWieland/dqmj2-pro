#include "context.h"
u32 native_main_02043e7c(void) {
    s32 order[2];
    s32 i;
    s32 j;
    u32 result;
    u8 *slot;
    s32 side;
    result=0;
    if(!native_data_main_020f69c4) {
        if(!native_fn_020444ec() || (u8)native_fn_itcm_01ffa824()<native_fn_itcm_01ffa84c()) {
            order[0]=0;order[1]=1;
        } else {order[0]=1;order[1]=0;}
        i=0;
        do {
            side=order[i];
            slot=ov001_side_slot_record_021db438(side,0);
            j=0;
            do {
                if(ov001_record_is_active_021db8d0(slot))result|=native_fn_ov001_0220ed5c(slot);
                j++;
                slot+=0x440;
            }while(j<3);
            {
                u8 *secondSlot=ov001_side_slot_record_021db438(side+2,0);
                s32 k=0;
                do {
                    if(ov001_record_is_active_021db8d0(secondSlot))result|=native_fn_ov001_0220ed5c(secondSlot);
                    k++;
                    secondSlot+=0x440;
                }while(k<3);
            }
            i++;
        }while(i<2);
    }
    return result;
}
