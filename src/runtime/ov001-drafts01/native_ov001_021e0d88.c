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
#define MULT_HI(a, b) ((s32)(((s64)(s32)(a) * (s32)(b)) >> 32))
#define MULTU_HI(a, b) ((u32)(((u64)(u32)(a) * (u32)(b)) >> 32))
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
extern u32 native_fn_020443fc();
extern u32 native_fn_ov001_021d7584();
extern u32 native_fn_ov001_021db2ec();
extern u32 ov001_side_slot_record_021db438();
extern u32 ov001_record_is_active_021db8d0();
extern u32 native_fn_ov001_021dc940();
extern u32 native_fn_ov001_021e29e8();
extern u32 native_fn_ov001_021e2a48();
extern u32 native_fn_ov001_021e6710();
extern u32 native_fn_ov001_021f111c();
extern u32 native_fn_ov001_021f11e8();
extern u32 native_fn_ov001_02210c74();
u32 native_ov001_021e0d88(void) {
    s32 var_r7;
    s32 var_r8;
    u32 temp_r5;

    native_fn_ov001_021d7584(4);
    native_fn_ov001_021d7584(3);
    native_fn_ov001_021d7584(5);
    native_fn_ov001_021d7584(6);
    native_fn_ov001_021d7584(7);
    native_fn_ov001_021d7584(8);
    native_fn_ov001_021d7584(9);
    native_fn_ov001_021d7584(0xA);
    native_fn_ov001_021d7584(0xB);
    native_fn_ov001_021d7584(0xC);
    native_fn_ov001_021d7584(0x13);
    native_fn_ov001_021d7584(0x14);
    native_fn_ov001_021d7584(0x15);
    native_fn_ov001_021d7584(0x16);
    native_fn_ov001_021d7584(0x17);
    native_fn_ov001_021d7584(0x18);
    native_fn_ov001_021d7584(0x19);
    native_fn_ov001_021d7584(0xE);
    native_fn_ov001_021d7584(0xF);
    native_fn_ov001_021d7584(0x10);
    native_fn_ov001_021d7584(0x11);
    native_fn_ov001_021d7584(0x12);
    native_fn_ov001_021d7584(2);
    native_fn_ov001_021d7584(0x2B);
    native_fn_ov001_021d7584(0x1A);
    native_fn_ov001_021d7584(0x1B);
    native_fn_ov001_021d7584(0x1D);
    native_fn_ov001_021d7584(0x22);
    native_fn_ov001_021d7584(0x23);
    native_fn_ov001_021d7584(0x25);
    native_fn_ov001_021d7584(0x1E);
    native_fn_ov001_021d7584(0x1F);
    native_fn_ov001_021d7584(0x21);
    native_fn_ov001_021d7584(0x26);
    native_fn_ov001_021d7584(0x27);
    native_fn_ov001_021d7584(0x29);
    native_fn_ov001_021f111c();
    native_fn_ov001_021f11e8();
    native_fn_ov001_02210c74();
    if (native_fn_ov001_021e6710() == 7) {
        native_fn_020443fc();
        native_fn_ov001_021db2ec();
        if (native_fn_ov001_021e29e8() & 2) {
            native_fn_ov001_021e2a48(2);
        }
        var_r7 = 0;
        do {
            var_r8 = 0;
loop_5:
            temp_r5 = ov001_side_slot_record_021db438(var_r7, var_r8);
            if (ov001_record_is_active_021db8d0() != 0) {
                native_fn_ov001_021dc940(temp_r5, 0x36);
            }
            var_r8 += 1;
            if (var_r8 < 3) {
                goto loop_5;
            }
            var_r7 += 1;
        } while (var_r7 < 2);
    }
    return 1U;
}
