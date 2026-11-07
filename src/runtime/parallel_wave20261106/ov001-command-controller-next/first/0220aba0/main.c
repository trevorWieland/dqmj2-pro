#include "context.h"
void native_ov001_0220aba0(s32 index,u32 a,u32 b,u8 c,u8 d,u8 e,u8 f,s8 g,u32 h){
 EntryView *entry=native_fn_02049ad0(index);
 native_fn_02049be4(entry,1,a,b,c,d,e,f,native_data_0223df3c.field4,g,h);
 entry->field0->field4->field18|=2;
 native_data_0223df3c.field4+=e*f;
 native_data_0223df44[native_data_0223df3c.field0++]=(s8)index;
}
