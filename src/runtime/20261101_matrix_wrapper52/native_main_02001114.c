typedef unsigned int u32;
typedef signed int s32;
extern void native_fn_02000d0c(const s32 *,s32 *,s32,s32,s32);
u32 native_main_02001114(const s32 *source,s32 *destination,s32 x,s32 y,s32 z) {
    u32 result;
    native_fn_02000d0c(source,destination,x,y,z);
    destination[9] = source[9];
    destination[10] = source[10];
    result = (u32)source[11];
    destination[11] = (s32)result;
    return result;
}
