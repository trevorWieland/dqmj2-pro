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

void native_ov007_021d7ad0(u32 value) {
    data_ov007_021da980[11] = value;
    data_ov007_021da980[10] = 0;
}

void native_ov007_021d7a4c(void) {
    func_ov007_021d7658();
    func_ov007_021d974c();
    func_02084920();
    func_0204617c(0, 5);
    func_0205dbc4(5, data_ov007_021da9b0);
    func_ov007_021d8cc8();
    func_0202a1e0(((s8 *)data_ov007_021da980)[0]);
    func_0202a164(5);
    func_ov007_021d9654();
    func_0203cb2c();
}

void native_ov007_021d7aa0(u32 value) {
    ((u16 *)data_ov007_021da980)[1] = value;
}

u32 native_ov007_021d7ab0(void) {
    return data_ov007_021da980[13];
}

u32 native_ov007_021d7ac0(void) {
    return data_ov007_021da980[1];
}

Choice native_ov007_021d85e4(void) {
    return data_ov007_021da0f4;
}
