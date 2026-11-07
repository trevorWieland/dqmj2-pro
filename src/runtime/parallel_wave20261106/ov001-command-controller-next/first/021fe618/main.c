#include "context.h"
EntryView *native_ov001_021fe618(s32 group,s32 index,u32 a,u32 b,u8 c,u8 d,u8 e,u8 f,u8 g,u8 h){
 EntryView *entry=native_fn_02049ad0(index);
 u32 added=native_fn_02068f70(index,a,8,b,c,d,native_data_02239c64[group]>>5,e,f,g,0,h);
 native_data_02239c64[group]+=added<<5;
 return entry;
}
