#include "context.h"
void native_ov000_02219ce4(NativeVector *position) {
    NativeRow *row;
    u32 width,height;
    s32 max_x,max_z;
    row=(NativeRow*)native_fn_ov000_021df3bc((s32)native_fn_ov000_021df1f0());
    if(row->field08<32)width=256;
    else width=row->field08*8;
    width=(u16)width;
    if(row->field09<24)height=192;
    else height=row->field09*8;
    height=(u16)height;
    max_x=(width-128)*4096;
    max_z=(height-96)*4096;
    if(position->x<0x80000)position->x=0x80000;
    if(position->x>max_x)position->x=max_x;
    if(position->z<0x60000)position->z=0x60000;
    if(position->z>max_z)position->z=max_z;
}
