#include "context.h"
s32 native_main_02072b74(u32 unused,Hit *hit,s32 notify,s8 *status)
{
    Sample *sample=native_fn_02066c3c();
    Row *row=native_data_021c5a11;
    s32 index=0;
    do {
        if(row->enabled!=0){
            if(sample->x>=row->x*8 && sample->x<(row->x+8)*8){
                if(sample->y>=row->y*8 && sample->y<(row->y+2)*8){
                    hit->field0=-1;
                    hit->index=(u8)index;
                    hit->field6=0;
                    if(native_fn_02072ed4((u8)index)!=0){
                        if(notify!=0){
                            if(index==0)native_fn_0205e7a8(-1,82);
                            else native_fn_0205e7a8(-1,83);
                        }
                        return (s8)index;
                    }
                    *status=2;
                    if(notify!=0)native_fn_0205e7a8(-1,84);
                    return -1;
                }
            }
        }
        index+=1;
        row+=1;
    } while(index<2);
    return -1;
}
