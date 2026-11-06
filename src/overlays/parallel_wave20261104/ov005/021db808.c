typedef unsigned short u16;
typedef unsigned int u32;
typedef struct State {
    unsigned char pad[0x40];
    u32 first;
    u32 second;
} State;
typedef struct Flags {
    unsigned char pad[0x7c];
    u32 value;
} Flags;
typedef struct Control {
    unsigned char pad[0x14];
    u32 value;
} Control;
extern State *native_fn_02063f6c(void);
extern const void *native_fn_020633b0(void);
extern void native_fn_02046af4(const void *, const void *, int, int, u16 *, int);
extern unsigned char native_data_021c9698[];
extern void native_fn_ov005_021ddec4(int, const u16 *);
extern const u16 *native_fn_0206442c(void);
extern void native_fn_ov005_021dddec(int, int, int, u16);
extern void native_fn_ov005_021df3bc(void);
extern int native_fn_020643fc(u16);
extern void native_fn_ov005_021df434(int, int, int);
extern void native_fn_020877bc(u32, u16 *, u32, u32);
extern const u32 *native_fn_020633bc(void);
extern void native_fn_ov005_021db5d0(u32);
extern int native_fn_0206434c(void);
extern void native_fn_ov005_021db6f8(int);
extern void native_fn_02067dd4(void);
extern int native_fn_02067d54(void);
extern Flags native_data_021e9a28;
extern Control native_data_021e9818;
void native_ov005_021db808(void)
{
    u16 buffer[32];
    State *state = native_fn_02063f6c();
    u32 second;
    u32 first;
    native_fn_02046af4(native_data_021c9698, native_fn_020633b0(), 31, 0, buffer, 255);
    native_fn_ov005_021ddec4(0, buffer);
    native_fn_ov005_021dddec(1, 19, 4, *native_fn_0206442c());
    native_fn_ov005_021df3bc();
    native_fn_ov005_021df434(native_fn_020643fc(*native_fn_0206442c()), 2, 4);
    second = state->second;
    first = state->first;
    if (second > 999)
        second = 999;
    if (first > 9999)
        first = 9999;
    native_fn_020877bc(first, buffer, 16, 4);
    native_fn_ov005_021ddec4(3, buffer);
    native_fn_020877bc(second, buffer, 16, 3);
    native_fn_ov005_021ddec4(6, buffer);
    native_fn_ov005_021db5d0(*native_fn_020633bc() / 30);
    native_fn_ov005_021db6f8(native_fn_0206434c());
    native_fn_02067dd4();
    native_fn_ov005_021dddec(14, 19, 3, native_fn_02067d54() + 21);
    native_data_021e9a28.value |= 2;
    native_data_021e9818.value = 1;
}
