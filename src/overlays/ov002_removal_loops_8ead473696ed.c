typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef short s16;
typedef unsigned int u32;
typedef int s32;

extern u8 data_ov002_021da560[];
extern u32 data_ov002_021db098[];
extern u8 data_ov002_021da5bc[];
extern u8 data_ov002_021daef8[];
extern u8 data_021c9698[];
extern u32 data_ov002_021db2a4[];
extern u8 data_ov002_021db2b8[];
extern u32 data_ov002_021db2c8[];

typedef struct {
    s8 a;
    s8 b;
    s8 c;
    u8 pad;
    s32 count;
    u32 value8;
    u32 value12;
    u32 value16;
} State;

typedef struct {
    u32 value0;
    u32 value4;
    u32 value8;
    u16 value12;
    u16 value14;
} Object;

extern State data_ov002_021daee4;
extern void func_ov002_021d7630(u32);
extern void func_ov002_021d76f0(u32);
extern void func_ov002_021d7744(u32, u32);
extern void func_ov002_021d7668(u32, u32);
extern u32 func_02065730(u32 *, s32, u32, u32, u32);
extern void func_02049008(Object *, u32, s8, s8, s8);
extern u32 func_02049f24(void);
extern void func_02049f30(void);
extern u32 *func_02049ad0(s32);
extern void func_02046af4(u8 *, u32, u32, u32, u32, u32);
extern void func_02049f14(u32);
extern void func_ov002_021d7998(u32, s32, u32, u32, u32, u32, u32, u32, u32);
extern void func_ov002_021d7ab0(u32, u32, u32, u32, s16);
extern void func_02049f4c(u32 *);
extern void func_02049ffc(u32);
extern void func_0201d444(void *, u8 *);
extern u32 func_0203cc2c(void *, u32);
extern void func_0204820c(u32, u32, u32);
extern void func_0202a498(u32, u32);
extern void func_02048308(void);
extern u32 *func_ov002_021da04c(void);
extern void func_ov002_021d828c(s32);
extern u32 func_02048f7c(u32);
extern void func_02045680(u32);
extern u32 func_0202a1e0(u32);
extern void func_02048e74(u8 *, u32);
extern void func_02048fcc(u32 *);
extern void func_ov002_021d9ca4(void);
extern void func_ov002_021d9ea8(void);
extern u32 func_02027400(void);

void native_ov002_021d81c8(s32 limit) {
    State *state;
    s8 *entries;
    u32 *values;
    s32 count;
    values = func_ov002_021da04c();
    state = &data_ov002_021daee4;
    count = state->count;
    if (count > limit) {
        entries = (s8 *)data_ov002_021daef8;
        do {
            s8 *last = entries + count;
            func_ov002_021d828c(last[-1]);
            count = state->count;
        } while (count > limit);
    }
    func_02045680(func_02048f7c(1));
    values[func_02048f7c(1)] = 32;
}

void native_ov002_021d822c(void) {
    State *state;
    s8 *entries;
    u32 *values;
    s32 count;
    values = func_ov002_021da04c();
    state = &data_ov002_021daee4;
    count = state->count;
    if (count > 0) {
        entries = (s8 *)data_ov002_021daef8;
        do {
            s8 *last = entries + count;
            func_ov002_021d828c(last[-1]);
            count = state->count;
        } while (count > 0);
    }
    func_02045680(func_02048f7c(1));
    values[func_02048f7c(1)] = 32;
}
