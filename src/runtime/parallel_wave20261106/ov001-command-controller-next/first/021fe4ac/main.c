#include "context.h"
EntryView *native_ov001_021fe4ac(s32 index,u32 a,u32 b,u8 c,u8 d,u8 e,u8 f,s8 g,u32 h){
 EntryView *entry=native_fn_02049ad0(index);
 native_fn_02049be4(entry,1,a,b,c,d,e,f,native_data_02239c10.field58>>5,g,h);
 if(h)native_data_02239c10.field58+=(e*f)<<5;
 return entry;
}
