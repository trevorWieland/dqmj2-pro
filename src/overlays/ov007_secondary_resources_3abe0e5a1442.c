typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;

extern u32 data_ov007_021da0f4[];
extern u32 data_ov007_021da9b8[];
extern u8 data_ov007_021da104[];
extern u8 data_ov007_021da120[];
extern u8 data_ov007_021da13c[];
extern u8 data_ov007_021da158[];
extern void func_ov007_021d7ae8(void);
extern void func_020725b8(void);
extern u32 func_ov007_021d8838(void);
extern u32 func_ov007_021d8634(void);
extern u32 func_ov007_021d864c(u32);
extern u32 func_ov007_021d867c(u32);
extern void func_ov007_021d7aa0(u32);
extern void func_ov007_021d9158(void);
extern void func_0201d444(void *, const void *, u32);
extern u32 func_0203cc2c(const void *, u32);
extern u32 func_02040d18(u32, const void *);
extern u32 func_02040d5c(u32, const void *);
extern void func_0204820c(u32, u32, u32);
extern void func_02048308(void);
extern void func_02045994(u32, u32, u32, u32);
extern void func_02045490(u32, u32, u32, u32);
extern void func_0202a498(u32, u32);

void native_ov007_021d7bf4(void) {
    func_ov007_021d7ae8();
    func_020725b8();
    data_ov007_021da0f4[2] = func_ov007_021d8838();
    data_ov007_021da0f4[0] = func_ov007_021d8634();
    data_ov007_021da0f4[1] = func_ov007_021d864c(data_ov007_021da0f4[2]);
    func_ov007_021d7aa0(func_ov007_021d867c(data_ov007_021da0f4[2]));
    ((u8 *)data_ov007_021da9b8)[0] = 0;
}

void native_ov007_021d7c4c(void) {
    void (*target)(void) = func_ov007_021d9158;
    target();
}

void native_ov007_021d7c58(void) {
}

u32 native_ov007_021d7c5c(void) {
    u8 first[32];
    u8 second[32];
    u8 third[32];
    u8 archive[32];
    u32 result = 0;
    func_0201d444(archive, data_ov007_021da104, ((s8 *)data_ov007_021da9b8)[0]);
    func_0201d444(first, data_ov007_021da120, ((s8 *)data_ov007_021da9b8)[0]);
    func_0201d444(second, data_ov007_021da13c, ((s8 *)data_ov007_021da9b8)[0]);
    func_0201d444(third, data_ov007_021da158, ((s8 *)data_ov007_021da9b8)[0]);
    if (data_ov007_021da9b8[2] == 0) {
        data_ov007_021da9b8[2] = func_0203cc2c(archive, 5);
        if (data_ov007_021da9b8[2] != 0) {
            data_ov007_021da9b8[5] = func_02040d18(data_ov007_021da9b8[2], first);
            data_ov007_021da9b8[6] = func_02040d5c(data_ov007_021da9b8[2], first);
            data_ov007_021da9b8[4] = func_02040d18(data_ov007_021da9b8[2], second);
            data_ov007_021da9b8[1] = func_02040d5c(data_ov007_021da9b8[2], second);
            data_ov007_021da9b8[3] = func_02040d18(data_ov007_021da9b8[2], third);
            data_ov007_021da9b8[7] = func_02040d5c(data_ov007_021da9b8[2], third);
            result = 1;
        }
    }
    return result;
}

void native_ov007_021d7de4(void) {
    data_ov007_021da9b8[4] = 0;
    data_ov007_021da9b8[5] = 0;
    data_ov007_021da9b8[3] = 0;
    func_0202a498(5, data_ov007_021da9b8[2]);
    data_ov007_021da9b8[2] = 0;
}
