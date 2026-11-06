typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef int s32;

extern u32 data_ov007_021da0f4[];
extern u8 data_ov007_021da9b8[];
extern u32 data_ov007_021daa0c[];
extern u8 data_ov007_021daa10[];
extern u8 data_ov007_021da910[];
extern u8 data_ov007_021da91c[];
extern s8 data_ov007_021da924[];
extern s32 data_ov007_021db2c8[];
extern void func_ov007_021d9424(void);
extern void func_ov007_021d7de4(void);
extern void func_02003dcc(void);
extern void func_02003de0(void);
extern u32 func_020725d8(u32);
extern u32 func_020726d8(void);
extern u32 func_ov007_021d876c(void);
extern void func_0203d0cc(u32);
extern void func_020851a8(void);
extern void func_0205e73c(u32);
extern void func_0205e7a8(s32, u32);
extern u32 func_0205f5dc(void);
extern void func_0205f5f4(u32);
extern void func_0203cfe0(void);
extern u32 func_0203cfe8(void);
extern void func_0201d444(void *, void *, u32);
extern void func_0204bc78(void *, void *, void *);
extern u32 func_0204bd6c(void *);
extern u32 func_ov007_021d9714(void);
extern void func_0204bcbc(void *);

void native_ov007_021d85c4(void) {
    void (*target)(void) = func_ov007_021d9424;
    target();
}

void native_ov007_021d85d0(void) {
    func_ov007_021d7de4();
    func_02003dcc();
    func_02003de0();
}

u32 native_ov007_021d85fc(void) {
    return data_ov007_021da0f4[2];
}

u32 native_ov007_021d860c(void) {
    u32 (*target)(u32) = func_020725d8;
    return target(data_ov007_021da0f4[2]);
}

void native_ov007_021d8624(u32 value) {
    data_ov007_021da9b8[0] = value;
}

u32 native_ov007_021d876c(void) {
    u32 mode = func_020726d8();
    u32 result = 0;
    switch (mode) {
    case 0:
    case 16: result = 170; break;
    case 2: result = 172; break;
    case 3: result = 173; break;
    case 4: result = 174; break;
    case 5: result = 175; break;
    case 7: result = 177; break;
    case 8: result = 178; break;
    case 9: result = 179; break;
    case 10: result = 180; break;
    case 18: result = 558; break;
    }
    return result;
}

void native_ov007_021d8828(void) {
    func_0203d0cc(func_ov007_021d876c());
}

void native_ov007_021d8938(void) {
    void (*target)(void) = func_020851a8;
    target();
}

void native_ov007_021d961c(u32 value) {
    void (*target)(u32) = func_0205e73c;
    target(value);
}

void native_ov007_021d9628(u32 value) {
    void (*target)(s32, u32) = func_0205e7a8;
    target(-1, value);
}

void native_ov007_021d963c(void) {
    data_ov007_021daa0c[0] = func_0205f5dc();
}

void native_ov007_021d9654(void) {
    void (*target)(u32) = func_0205f5f4;
    target(data_ov007_021daa0c[0]);
}

void native_ov007_021d966c(void) {
    u8 name[32];
    func_0203cfe0();
    func_0201d444(name, data_ov007_021da910, func_0203cfe8());
    func_0204bc78(data_ov007_021daa10, data_ov007_021da91c, name);
}

u32 native_ov007_021d9714(void) {
    u32 (*target)(void *) = func_0204bd6c;
    return target(data_ov007_021daa10);
}

u32 native_ov007_021d9728(void) {
    u32 result = 0;
    if (func_ov007_021d9714() != 0) {
        result = ((u32 *)data_ov007_021daa10)[1];
    }
    return result;
}

void native_ov007_021d974c(void) {
    void (*target)(void *) = func_0204bcbc;
    target(data_ov007_021daa10);
}

void native_ov007_021d9760(u32 value) {
    data_ov007_021da924[0] = value;
}

void native_ov007_021d9854(void) {
}

u32 native_ov007_021d9cac(void) {
    return data_ov007_021da924[0] != -1;
}

u32 native_ov007_021da04c(void) {
    return data_ov007_021db2c8[1] > data_ov007_021db2c8[2];
}
