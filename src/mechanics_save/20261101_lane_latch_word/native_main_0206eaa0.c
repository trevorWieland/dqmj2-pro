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
extern u32 native_fn_02049f4c(void **widget);
extern void native_fn_02061260(s8 value);
extern u8 *native_fn_02061944(void);
extern void **native_fn_02061dcc(s32 index);
extern u32 native_fn_020620b4(s8 index);
extern void native_fn_02062144(s32 index,u32 mode);
extern void native_fn_02062328(void);
extern u32 native_fn_02062358(u32 value);
extern u32 native_fn_0206238c(s8 *index,s32 lower,s32 upper);
extern u32 native_fn_0206259c(void);
extern u32 native_fn_0206dca4(void);
extern void native_fn_0206de44(u32 value);
extern void native_fn_0206e11c(void);
extern void native_fn_0206e148(void);
extern void native_fn_0206e214(void);
extern void native_fn_0206ec84(void);
extern void native_fn_0206ed18(void);
extern void native_fn_0206efe8(s32 row);
extern void native_fn_0206f070(s32 row);
typedef struct {
    u8 unknown_0[0x3];
    u8 field_3;
    u8 unknown_4[0x28];
    s8 field_2c;
} Record_native_data_021c4f60;
extern Record_native_data_021c4f60 native_data_021c4f60;
u32 native_main_0206eaa0(void) {
    s8 temp_r0_2;
    u8 *temp_r0;
    u32 var_r5;
    u32 var_r6;
    s8 var_r7;
    s8 temp_r8;
    s8 sp0;

    temp_r0 = native_fn_02061944();
    var_r5 = 0;
    sp0 = M2C_FIELD(temp_r0, s8 *, 0x269);
    temp_r0_2 = M2C_FIELD(temp_r0, s8 *, 0x26A);
    switch (temp_r0_2) {
    case 0:
        native_fn_0206ec84();
        native_fn_0206ed18();
        native_fn_02062144(M2C_FIELD(temp_r0, s8 *, 0x26F), 0);
        M2C_FIELD(temp_r0, s8 *, 0x26A) = 1;
        native_fn_0206de44(1);
        native_data_021c4f60.field_3 = 1U;
        native_fn_02061260(0);
        
    case 1:
        if (native_data_021c4f60.field_2c != 0) {
            native_fn_02062328();
            native_fn_02062144(M2C_FIELD(temp_r0, s8 *, 0x26F), 0);
            native_fn_0206e11c();
            native_fn_0206e214();
            native_fn_0206e148();
            var_r7 = 0;
            do {
                temp_r8 = var_r7 + 6;
                if ((native_fn_0206259c() == 0) && (temp_r8 == 9)) {

                } else {
                    native_fn_02049f4c(native_fn_02061dcc(temp_r8));
                    if (native_data_021c4f60.field_3 != 0) {
                        native_fn_0206efe8(temp_r8);
                    }
                    native_fn_0206f070(temp_r8);
                }
                var_r7 += 1;
            } while ((s32) var_r7 < 0xA);
            native_fn_0206de44(0);
            if (native_fn_0206dca4() != 0) {
                native_data_021c4f60.field_3 = 0U;
            } else {
                native_data_021c4f60.field_3 = 1U;
            }
        }
        var_r6 = native_fn_0206238c(&sp0, 1, 6);
        if (var_r6 != 1) {
            var_r6 = 0;
        }
        if (sp0 != M2C_FIELD(temp_r0, s8 *, 0x269)) {
            native_fn_020620b4(sp0);
            native_fn_02062358(var_r6);
            var_r5 = 1;
        }
        break;
    }
    if (M2C_FIELD(temp_r0, s8 *, 0x26C) != 0x2A) {
        var_r5 = 1;
    }
    return var_r5;
}
