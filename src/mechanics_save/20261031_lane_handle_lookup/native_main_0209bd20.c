typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;
extern u32 native_fn_020b45ac(void *handle);
extern u32 native_data_021d19e0;
extern u32 native_data_021d19e8[32];

u32 native_main_0209bd20(s32 query) {
    s32 index;
    u32 *slot;
    if (native_data_021d19e0==0) return 0;
    slot=native_data_021d19e8;
    index=0;
loop:
    if ((*slot!=0)&&(query==((u8 *)native_fn_020b45ac((void *)*slot))[1])) return native_data_021d19e8[index];
    index+=1;
    slot+=1;
    if (index>=32) return 0;
    goto loop;
}
