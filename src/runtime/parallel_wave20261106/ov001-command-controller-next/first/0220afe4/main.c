#include "context.h"
void native_ov001_0220afe4(Record10View *record,u32 value){
 u16 buffer[16];
 native_fn_ov001_0220aba0(6,record->field10,2,1,3,16,2,0,1);
 native_fn_ov001_0220ac58(6,5,4,1,16);
 native_fn_ov001_0220aba0(7,record->field10,2,1,5,16,2,0,1);
 native_fn_02046af4(native_data_021c9698,native_fn_02062a10(value),13,16,buffer,255);
 Half4View *flags=native_fn_020449d4(native_fn_02062a10(value)->field18);
 native_fn_ov001_0220ac9c(7,buffer,(u8)flags->field4high,16,0,1);
}
