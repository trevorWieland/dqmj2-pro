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

void native_ov003_021d81a8(void) {
    char buffer[32];
    s8 index;
    Runtime *runtime = func_02061944();
    func_0201d444(buffer, data_ov003_021e0278);
    func_0205ff80(buffer);
    for (index = 0; index < 14; index++) {
        u32 delta = func_02065730(&runtime->cells[index + 1], data_ov003_021e0128[index].id, 0, data_ov003_021e0128[index].count, runtime->offset);
        runtime->offset = runtime->offset + delta;
    }
    func_0205ff9c();
}
