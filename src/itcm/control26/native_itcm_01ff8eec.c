typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
typedef float f32;
typedef double f64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_fn_01ffa33c(void);
extern u32 native_fn_01ffa394(u32);
extern u32 native_fn_01ffb4ec(u32);
extern u32 native_fn_02008e0c(u32, u32, u32);
extern u8 native_data_01fff930[];
extern u8 native_data_021ceb54[];
extern u8 native_data_021cebb3[];
void native_itcm_01ff8eec(void) {

    if (native_fn_01ffa394((u32) *native_data_01fff930) == 1) {
        M2C_FIELD(native_data_021ceb54, s16 *, 0x5C) = (s16) native_fn_01ffa33c();
        M2C_FIELD(native_data_021ceb54, u8 *, 0x5E) = (u8) *native_data_01fff930;
        native_fn_02008e0c(native_fn_01ffb4ec((u32) *native_data_01fff930), (u32) native_data_021cebb3, 0x14U);
    }
    ++*native_data_01fff930;
    if (*native_data_01fff930 >= 8) *native_data_01fff930 = 0;
}
