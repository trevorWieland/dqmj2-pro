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
extern u32 native_fn_01ffa348(u32);
extern u32 native_fn_01ffa5ac(u32, u32, u32);
extern u32 native_fn_01ffa5fc(u32, u32);
extern u32 native_fn_01ffa6c0(u32, u32);
extern u32 native_fn_01ffa804(void);
extern u32 native_fn_01ffa8b8(u32);
extern u32 native_fn_01ffac9c(u32, u32, u32, u32, u32, u32);
extern u32 native_fn_01ffae9c(u32, u32, u32, u32);
extern u32 native_fn_01ffafb8(void);
extern u32 native_fn_01ffb060(u32);
extern u32 native_fn_01ffb35c(void);
extern u32 native_fn_01ffb4ec(u32);
extern u32 native_fn_02008e0c(u32, u32, u32);
extern u32 native_fn_0205e7a8(u32, u32);
extern u32 native_fn_020620e8(u32, u32);
extern u32 native_fn_02084730(void);
extern u32 native_fn_ov000_02223c54();
extern u8 native_data_021ceb54[];
extern u8 native_data_021ceb94[];
void native_itcm_01ff951c(u32 arg0, u32 arg1, u32 arg2, u32 arg3) {
    u32 temp_r0;
    u32 temp_r0_2;
    u32 temp_r4;

    temp_r4 = native_fn_ov000_02223c54();
    native_fn_01ffa5ac((u32) native_data_021ceb94, 0x34U, 2U);
    temp_r0 = native_fn_01ffa6c0(0U, 1U);
    if (temp_r0 != 0) {
        native_fn_01ffa348((u32) M2C_FIELD(temp_r0, u16 *, 0x1C));
        native_fn_02008e0c(temp_r0 + 0x1F, native_fn_01ffb4ec((u32) M2C_FIELD(temp_r0, u8 *, 0x1E)), 0x14U);
    }
    if ((M2C_FIELD(temp_r4, s8 *, 0x58) == 1) && (M2C_FIELD((void *) native_fn_01ffb35c(), u16 *, 2) & 2)) {
        native_fn_0205e7a8(-1U, 0x53U);
        native_fn_01ffa804();
        native_fn_01ffa348(1U);
        native_fn_020620e8(0x1BU, 1U);
        native_fn_01ffafb8();
        native_fn_01ffb060(0U);
        native_fn_01ffac9c(2U, 1U, 0xDU, 1U, 2U, 2U);
        M2C_FIELD(native_data_021ceb54, s32 *, 0xC) = 4;
        return;
    }
    temp_r0_2 = native_fn_01ffa5fc(0U, 2U);
    if ((temp_r0_2 != 0) && (M2C_FIELD(temp_r0_2, s32 *, 0x14) != 0)) {
        native_fn_01ffafb8();
        if (M2C_FIELD(temp_r0_2, s32 *, 0x14) == 1) {
            native_fn_0205e7a8(-1U, 0x57U);
            M2C_FIELD(native_data_021ceb54, s32 *, 0xC) = 0x1B;
            native_fn_01ffa8b8(M2C_FIELD(temp_r0_2, u32 *, 0x18));
            native_fn_02084730();
            return;
        }
        M2C_FIELD(native_data_021ceb54, s32 *, 0xC) = 0x1C;
        if (M2C_FIELD(native_data_021ceb54, s32 *, 8) == 1) {
            if (M2C_FIELD(temp_r4, s8 *, 0x58) == 1) {
                native_fn_01ffae9c(0x10U, 0xFU, 5U, 0x57U);
                return;
            }
            native_fn_01ffae9c(0x10U, 6U, 0xEU, 0x57U);
            return;
        }
        native_fn_01ffae9c(0x10U, 9U, 4U, 0x57U);
    }
}
