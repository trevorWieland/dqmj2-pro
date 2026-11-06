typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;

typedef struct { u32 first; u32 second; u32 third; u32 fourth; } Choice;

extern u32 data_ov007_021da980[];
extern u8 data_ov007_021da9b0[];
extern Choice data_ov007_021da0f4;
extern void func_ov007_021d8af8(void);
extern void func_ov007_021d966c(void);
extern u32 func_ov007_021d96b0(u32);
extern void func_02041898(u32);
extern Choice func_ov007_021d85e4(void);
extern void func_ov007_021d74e4(u32);
extern void func_ov007_021d8abc(u32);
extern void func_ov007_021d88dc(u32);
extern u32 func_02041944(void);
extern u32 func_02041814(void);
extern void func_ov007_021d75f0(void);
extern void func_02041510(u32, u32, u32);
extern u32 func_ov007_021d8664(u32);
extern void func_ov007_021d8bc0(void);
extern u32 func_ov007_021d7ac0(void);
extern u32 func_ov007_021da04c(void);
extern u32 func_ov007_021d9cac(void);
extern void func_ov007_021d953c(void);
extern void func_020414b0(u32);
extern u32 func_02041800(void);
extern void func_ov007_021d89a8(void);
extern void func_0203d138(u32);
extern void func_ov007_021d85c4(void);
extern u32 func_ov007_021d8984(u32);
extern void func_ov007_021d7658(void);
extern u32 func_ov007_021d9728(void);
extern void func_ov007_021d7690(void);
extern void func_02041764(void);
extern void func_ov007_021d769c(void);
extern void func_ov007_021d974c(void);
extern void func_02084920(void);
extern void func_0204617c(u32, u32);
extern void func_0205dbc4(u32, void *);
extern void func_ov007_021d8cc8(void);
extern void func_0202a1e0(u32);
extern void func_0202a164(u32);
extern void func_ov007_021d9654(void);
extern void func_0203cb2c(void);

static void set_phase(u32 value) {
    data_ov007_021da980[11] = value;
    data_ov007_021da980[10] = 0;
}

u32 native_ov007_021d76a0(void) {
    Choice selected;
    u32 result = 5;
    data_ov007_021da980[13] = data_ov007_021da980[11];
    data_ov007_021da980[1] = data_ov007_021da980[10];
    switch (data_ov007_021da980[11]) {
    case 0:
        func_ov007_021d8af8();
        func_ov007_021d966c();
        if (func_ov007_021d96b0(128) != 0) {
            set_phase(9);
        } else {
            set_phase(1);
        }
        break;
    case 1:
        set_phase(2);
        break;
    case 2:
        func_02041898(2);
        selected = func_ov007_021d85e4();
        func_ov007_021d74e4(((u16 *)data_ov007_021da980)[1]);
        set_phase(3);
        func_ov007_021d8abc(1);
        break;
    case 3:
        func_ov007_021d88dc(0);
        if (func_02041944() == 0) {
            set_phase(4);
            ((u8 *)data_ov007_021da980)[1] = 0;
        } else {
            set_phase(5);
        }
        break;
    case 4:
        if (func_02041814() != 1 && ((u8 *)data_ov007_021da980)[1] == 0) {
            Choice selected2 = func_ov007_021d85e4();
            func_ov007_021d75f0();
            func_02041510(0, 2, 10);
            if (func_ov007_021d8664(selected2.third) != 2) {
                func_ov007_021d8abc(1);
            } else {
                func_ov007_021d8abc(0);
            }
            set_phase(6);
            func_ov007_021d8bc0();
        } else {
            ((u8 *)data_ov007_021da980)[1] = ((u8 *)data_ov007_021da980)[1] - 1;
        }
        break;
    case 5:
        if (func_ov007_021d7ac0() == 0) {
            data_ov007_021da980[10] = 4;
        } else if (func_ov007_021d7ac0() == 4) {
            if (func_ov007_021da04c() != 0) {
                if (func_ov007_021d9cac() != 0) {
                    set_phase(10);
                    func_ov007_021d953c();
                    ((u8 *)data_ov007_021da980)[1] = 0;
                } else {
                    set_phase(4);
                    ((u8 *)data_ov007_021da980)[1] = 40;
                }
            }
        }
        break;
    case 6:
        func_ov007_021d8bc0();
        break;
    case 7:
        if (data_ov007_021da980[10] == 0) {
            func_020414b0(63);
            func_02041510(1, 2, 30);
            data_ov007_021da980[10] = 2;
        } else if (data_ov007_021da980[10] == 2) {
            if (func_02041800() == 2) {
                if (func_ov007_021d96b0(129) != 0) {
                    data_ov007_021da980[11] = 9;
                    data_ov007_021da980[10] = 5;
                } else {
                    data_ov007_021da980[10] = 5;
                }
                func_ov007_021d89a8();
            }
        } else if (data_ov007_021da980[10] == 5) {
            func_0203d138(1);
            data_ov007_021da980[10] = 0;
            result = 11;
            func_ov007_021d85c4();
        }
        break;
    case 8:
        if (func_ov007_021d8984(0) != 0) {
            func_ov007_021d7658();
            set_phase(2);
        }
        break;
    case 9:
        switch (func_ov007_021d9728()) {
        case 128: set_phase(1); break;
        case 140: set_phase(7); break;
        case 129:
            data_ov007_021da980[11] = 7;
            data_ov007_021da980[10] = 5;
            break;
        }
        break;
    case 10:
        break;
    }
    func_ov007_021d7690();
    func_02041764();
    func_ov007_021d769c();
    return result;
}
