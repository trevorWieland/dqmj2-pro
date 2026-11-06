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
extern u32 native_fn_02008e0c(u32, u32, u32, u32);
extern u32 native_data_01fff958;
extern u32 native_data_021ceca0;
extern u32 native_data_021ceca4;
void native_itcm_01ffb7ac(u32 arg0, u32 arg1, u32 arg2) {
    u16 temp_r3;

    M2C_FIELD(&native_data_021ceca0, u16 *, 2) = (u16) M2C_FIELD(arg1, u16 *, 2);
    temp_r3 = M2C_FIELD(arg1, u16 *, 0);
    M2C_FIELD(&native_data_021ceca0, u16 *, 0) = temp_r3;
    if (M2C_FIELD(arg1, u16 *, 0) != 0) {
        native_fn_02008e0c(arg1 + 4, (u32) &native_data_021ceca4, arg2, (u32) temp_r3);
    }
    native_data_01fff958 = 1;
}
