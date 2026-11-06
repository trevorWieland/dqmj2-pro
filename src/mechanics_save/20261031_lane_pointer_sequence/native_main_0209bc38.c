typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;
extern s32 native_fn_0209bbfc(const u8 **);
extern u32 native_fn_0209beac(const u8 *,s32);
extern u8 native_data_021d19e0[];
u32 native_main_0209bc38(void) {
    const u8 *pointer;
    s32 count;
    if(*(u32 *)native_data_021d19e0==0) return 0;
    count=native_fn_0209bbfc(&pointer);
    return native_fn_0209beac(pointer,count);
}
