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
extern void native_fn_02008140(u32);
extern u8 * native_fn_0202a634(void);
extern void native_fn_020406a8(u32);
extern void native_fn_0204075c(u32);
extern void native_fn_02041510(u32,u32,u32);
extern void native_fn_02041538(u32,u32,u32);
extern void native_fn_02041560(s32);
extern void native_fn_0204157c(s32);
extern int native_fn_02041800(void);
extern int native_fn_02041814(void);
extern void native_fn_020418e8(u32,s32);
extern s32 native_fn_02041930(void);
extern s32 native_fn_02041944(void);
extern void native_fn_0204b61c(void *,u32);
extern void native_fn_0205e704(u32);
extern void native_fn_0205fa4c(void *,u32);
extern void native_fn_02061934(u32);
extern void native_fn_02062074(u32);
extern int native_fn_02062520(void);
extern u32 * native_fn_02063ab0(void);
extern void native_fn_02079130(u32);
extern void native_fn_0207979c(void);
extern void native_fn_020798b8(void);
extern void native_fn_02079d6c(u32);
extern void native_fn_02079f9c(u32);
extern void native_fn_02079fc0(u32);
extern void native_fn_0207a154(void);
extern void native_fn_0207a168(void *);
extern int native_fn_0207dd5c(s32);
extern int native_fn_0207dea8(void);
extern u32 native_fn_0207e3f8(void);
extern int native_fn_0207e4ac(void);
extern void native_fn_020c225c(u32);
extern void native_fn_ov000_021e7b9c(u32);
extern void native_fn_ov000_02214fc8(u32);
extern u8 * ov000_display_context_02215698(void);
extern void native_fn_ov000_022156a4(u32);
extern u32 native_fn_ov000_022156c4(void);
extern void native_fn_ov000_022156d4(void);
extern void native_fn_ov000_0221570c(u32);
extern void native_fn_ov000_0221573c(u32);
extern void native_fn_ov000_02217440(void);
extern u32 ov000_poll_change_notify_0221794c(void *);
extern void native_fn_ov000_02217bdc(u32,u32,u32,u32,u32,s32);
extern void native_fn_ov000_02217c9c(u32);
extern u32 native_data_020de468;
typedef struct {
    u32 field_0;
    s32 field_4;
    u8 unknown_8[0x4];
    u32 field_c;
} Record_native_data_021c6544;
extern Record_native_data_021c6544 native_data_021c6544;
extern u8 native_data_021c6560[];
extern u32 native_data_021c6638[];
u32 native_main_02079170(void) {
    u16 temp_r0;
    u16 temp_r1;
    u32 temp_r4;
    u8 *temp_r5;
    u32 temp_r5_2;
    u32 *var_r6;
    u8 *temp_r7;
    u32 var_r8;

    native_fn_ov000_02217440();
    temp_r4 = native_fn_ov000_022156c4();
    temp_r5 = ov000_display_context_02215698();
    var_r6 = 0;
    temp_r7 = native_fn_0202a634();
    var_r8 = 0;
    switch (native_data_021c6544.field_c) {
    default:
        break;
    case 0:
        var_r6 = native_data_021c6638;
        native_fn_02079d6c(1);
        native_fn_0204b61c(temp_r5 + 0x10, 1);
        native_data_021c6544.field_0 = (*native_fn_02063ab0()/30U);
        var_r8 = 1;
        native_data_020de468 = 1;
        break;
    case 1:
        var_r6 = native_data_021c6638;
        if (native_fn_02062520() != 0) {
            temp_r5_2 = (*native_fn_02063ab0()/30U);
            if (native_data_021c6544.field_0 != temp_r5_2) {
                native_data_021c6544.field_0 = temp_r5_2;
                native_fn_02079fc0(1U);
            }
            temp_r0 = M2C_FIELD(temp_r7, u16 *, 2);
            if (temp_r0 & 1) {
                if (*var_r6 == 0) {
                    native_data_020de468 = 2;
                } else if (*var_r6 == 1) {
                    native_fn_ov000_022156d4();
                }
            } else if (temp_r0 & 2) {
                native_fn_ov000_022156d4();
            } else {
                var_r8 = ov000_poll_change_notify_0221794c(var_r6);
            }
        }
        break;
    case 2:
        native_fn_0204b61c(temp_r5 + 0x10, 0);
        if (native_fn_0207e4ac() == 0) {
            native_data_020de468 = 6;
        } else if (native_fn_0207dd5c(2) == 0) {
            native_data_020de468 = 5;
        } else {
            native_fn_ov000_02217bdc(5, 6, 8, 1, 0, 0x52);
            native_fn_0205fa4c(native_data_021c6560, 1);
            native_data_020de468 = 3;
        }
        break;
    case 3:
        if (native_fn_0207dea8() != 0) {
            if (native_fn_0207e3f8() == 0) {
                native_fn_ov000_02217c9c(0);
                native_fn_ov000_02217bdc(5, 6, 9, 0, 0, 0x57);
                native_fn_0205fa4c(native_data_021c6560, 0);
                native_data_020de468 = 4;
                native_fn_0207979c();
                native_fn_020798b8();
                var_r8 = 1;
            } else {
                native_data_020de468 = 5;
            }
        } else {
            native_fn_0207a154();
        }
        break;
    case 4:
        if (M2C_FIELD(temp_r7, u16 *, 2) & 0xFF7) {
            native_data_020de468 = 7;
            native_fn_ov000_021e7b9c(0x52);
        }
        break;
    case 5:
    case 6:
        native_fn_020c225c(0x20000000);
        break;
    case 7:
        native_fn_ov000_02217c9c(1);
        native_fn_02079f9c(1);
        native_fn_02079d6c(8);
        native_data_020de468 = 8;
        native_fn_0204b61c(temp_r5 + 0x10, 1);
        break;
    case 8:
        var_r6 = native_data_021c6638;
        var_r8 = ov000_poll_change_notify_0221794c(var_r6);
        temp_r1 = M2C_FIELD(temp_r7, u16 *, 2);
        if (temp_r1 & 1) {
            switch (*var_r6) {
            case 0:
                native_fn_02079130(1);
                break;
            case 1:
                native_fn_ov000_02217bdc(5, 6, 0xA, 1, 1, 0x52);
                native_fn_0204b61c(temp_r5 + 0x10, 0);
                native_data_020de468 = 9;
                native_data_021c6544.field_4 = 1;
                native_fn_0204075c(7);
                break;
            }
        } else if (temp_r1 & 2) {
            native_fn_02079130(0);
        }
        break;
    case 9:
        if (M2C_FIELD(temp_r7, u16 *, 2) & 0xFF7) {
            native_fn_ov000_02217c9c(1);
            switch (native_data_021c6544.field_4) {
            case 1:
            case 2:
                native_fn_0204b61c(temp_r5 + 0x10, 1);
                native_fn_02062074(0);
                native_data_020de468 = 0xA;
                break;
            case 0:
                native_fn_ov000_022156d4();
                native_fn_ov000_0221570c(1);
                break;
            }
        }
        break;
    case 10:
        native_fn_0205e704(0xA);
        if (native_data_021c6544.field_4 == 1) {
            native_fn_0204157c(native_fn_02041944());
            native_fn_02041538(1, 2, 0xA);
            native_data_020de468 = 0xB;
        } else {
            native_fn_ov000_0221573c(7);
            native_fn_02061934(2);
            native_fn_ov000_022156a4(0x7F);
            native_fn_02062074(0);
            native_fn_ov000_0221570c(1);
            native_fn_ov000_02214fc8(2);
            native_fn_020406a8(0);
        }
        break;
    case 11:
        if ((native_fn_02041814() != 1) && (native_fn_02041800() != 1)) {
            native_fn_02041560(native_fn_02041930());
            native_fn_02041510(1, 2, 0xA);
            native_fn_020418e8(0xA, 0 - native_fn_02041930());
            native_data_020de468 = 0xC;
        }
        break;
    case 12:
        if ((native_data_021c6544.field_4 == 1) && (native_fn_02041814() != 1) && (native_fn_02041800() != 1)) {
            native_fn_02008140(0x40000000);
        }
        break;
    }
    if (var_r8 != 0) {
        native_fn_02079fc0(native_data_021c6544.field_c);
    }
    if (var_r6 != 0) {
        native_fn_0207a168(var_r6);
    }
    if (native_data_020de468 != 0xD) {
        native_data_021c6544.field_c = (u32) native_data_020de468;
        native_data_020de468 = 0xD;
    }
    return temp_r4;
}
