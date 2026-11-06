typedef unsigned int u32;
typedef int s32;

extern u32 *func_02049ae4(void);
extern s32 *func_ov002_021da04c(void);
extern u32 func_02048f7c(u32);
extern s32 func_02049af0(u32, u32, u32, s32, u32, u32, u32);
extern void func_020853c8(u32, u32);
extern void func_ov002_021d7630(u32);
extern void func_02086b14(u32, u32);

u32 native_ov002_021d7af8(u32 first, u32 second, u32 third, u32 fourth, u32 fifth, u32 sixth) {
    s32 result;
    s32 *values;
    u32 *previous;
    s32 offset;
    u32 *target;
    previous = func_02049ae4();
    values = func_ov002_021da04c();
    offset = values[func_02048f7c(1)] >> 5;
    result = func_02049af0(first, second, third, offset, fourth, fifth, sixth);
    values[func_02048f7c(1)] = result << 5;
    if (previous[0] != 0) {
        func_020853c8(previous[1], previous[0]);
    }
    func_ov002_021d7630(0);
    func_02086b14(func_02049ae4()[1], 10);
    target = (u32 *)func_02049ae4()[1];
    target[6] |= 2;
    return func_02049ae4()[1];
}
