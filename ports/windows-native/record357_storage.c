typedef unsigned char u8;
typedef signed int s32;
typedef unsigned int u32;
u8 record_context[0x1000];
u8 record_table[3200];
struct EktState { u32 count; void *records; } native_ekt_state;
u32 record_words[7];
u32 record_metric_calls;
u32 record_lower_calls;
extern u8 saved_native_category(s32);
u8 native_fn_02044cdc(s32 index) { record_metric_calls++; return saved_native_category(index); }
u32 native_fn_0206d2e0(s32 a0,s32 a1,u32 a2,u32 a3,s32 a4,s32 a5,s32 a6) {
 record_words[0]=(u32)a0;record_words[1]=(u32)a1;record_words[2]=a2;record_words[3]=a3;record_words[4]=(u32)a4;record_words[5]=(u32)a5;record_words[6]=(u32)a6;
 record_lower_calls++;return 0xDA010203U;
}
void record_reset(u32 species,u32 nibble,u32 index,u32 y,u32 base) {
 u32 i;
 for(i=0;i<0x1000;i++)record_context[i]=0xA5;
 for(i=0;i<3200;i++)record_table[i]=0xB6;
 record_context[0]=(u8)index;record_context[1]=(u8)y;record_context[4]=(u8)base;record_context[5]=(u8)(base>>8);
 record_table[species*100+4]=0xA5;record_table[species*100+5]=(u8)nibble;
 native_ekt_state.count=32;native_ekt_state.records=record_table;record_metric_calls=record_lower_calls=0;
 for(i=0;i<7;i++)record_words[i]=0xC7C7C7C7U;
}
