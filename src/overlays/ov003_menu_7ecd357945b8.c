typedef unsigned char u8;
typedef signed char s8;
typedef signed short s16;
typedef unsigned int u32;
typedef int s32;
typedef struct { u32 words[52]; } Payload;
typedef struct { signed char active:1; signed char reserved:1; signed char done:1; signed char started:1; signed char rest:4; } Bits;
typedef struct { Payload payload; volatile s8 index; Bits flags; u8 reserved[18]; } Menu;
typedef struct { u8 bytes[12]; } Cell;
typedef struct { u8 prefix[16]; Cell cells[49]; u32 offset; u8 middle[12]; s8 mode; u8 padding[2]; s8 selector; } Runtime;
typedef struct { s8 id; u8 count; } Entry;

extern u8 data_ov003_021e0464[];
extern Menu data_ov003_021e0498;
extern Entry data_ov003_021e0128[];
extern char data_ov003_021e0278[];
extern void func_02061bf0(void);
extern void func_02060f14(void);
extern void func_020c39d0(u32);
extern void func_ov003_021d81a8(void);
extern void func_ov003_021d823c(void);
extern void func_ov003_021d88e8(void);
extern Runtime *func_02061944(void);
extern void func_02062328(void);
extern void func_02062144(s32, u32);
extern void func_ov003_021d867c(void);
extern void func_ov003_021d89d8(void);
extern void func_ov003_021d8cac(void);
extern Payload *func_0205fc10(void *, void (*)(void), void (*)(void), u32, u32, u32, u32, u32);
extern void func_0205fd0c(void *);
extern u32 func_02041930(void);
extern void func_02041510(u32, u32, u32);
extern void func_ov003_021d8ce8(void);
extern void func_ov003_021d8890(void);
extern void func_020622ec(u32, u32, u32);
extern void func_0201d444(void *, const void *, ...);
extern void func_0205ff80(void *);
extern u32 func_02065730(void *, s32, u32, u32, u32);
extern void func_0205ff9c(void);
extern void func_02061c1c(u32, u32, u32, u32, u32, u32, u32);
extern void func_02045ed0(u32);
extern u8 *func_02062a10(u32);
extern void func_ov003_021d8348(void *, s32, u32, u32, u32);

void native_ov003_021d7fb8(void) {
    func_02061bf0();
    func_02060f14();
    func_020c39d0(1);
    func_ov003_021d81a8();
    func_ov003_021d823c();
    func_ov003_021d88e8();
    data_ov003_021e0464[1] = 0;
    data_ov003_021e0464[0] = 0;
}

u32 native_ov003_021d7ff0(void) {
    Runtime *runtime = func_02061944();
    u32 result = 0;
    switch (data_ov003_021e0464[0]) {
        case 0:
            func_02062328();
            func_02062144(runtime->selector, 0);
            func_ov003_021d867c();
            data_ov003_021e0498.flags.started = -1;
            if (runtime->mode == 42 && data_ov003_021e0498.flags.active == 0) {
                data_ov003_021e0498.index = 0;
                data_ov003_021e0498.flags.active = -1;
                data_ov003_021e0498.flags.reserved = 0;
                data_ov003_021e0498.flags.started = 0;
                data_ov003_021e0498.payload = *func_0205fc10(&data_ov003_021e0498, func_ov003_021d89d8, func_ov003_021d8cac, 0, 18, 8192, 2, 0);
                func_0205fd0c(&data_ov003_021e0498);
            }
            if (func_02041930()) {
                func_02041510(0, 2, 30);
            }
            data_ov003_021e0464[0] = 1;
            break;
        case 1:
            if (data_ov003_021e0498.flags.active && data_ov003_021e0498.flags.done) {
                func_0205fd0c(&data_ov003_021e0498);
                data_ov003_021e0498.flags.done = 0;
            }
            break;
    }
    if (runtime->mode != 42) {
        if (data_ov003_021e0498.flags.active) {
            func_ov003_021d8ce8();
        }
        result = 1;
    }
    return result;
}

void native_ov003_021d8188(void) {
    func_ov003_021d8ce8();
    func_ov003_021d8890();
    func_020622ec(6, 10, 0);
}

void native_ov003_021d823c(void) {
    func_02061c1c(6, 11, 3, 11, 2, 0, 0);
    func_02061c1c(7, 5, 5, 5, 2, 0, 0);
    func_02061c1c(8, 20, 3, 11, 2, 0, 0);
    func_02061c1c(9, 26, 5, 5, 2, 0, 0);
    func_02045ed0(1);
}

void native_ov003_021d82f4(u32 index) {
    Runtime *runtime = func_02061944();
    u8 *record = func_02062a10(index);
    if (record) {
        func_ov003_021d8348(&runtime->cells[data_ov003_021e0464[1] + 3], *(s16 *)(record + 24), data_ov003_021e0464[1], 1, 0);
    }
}
