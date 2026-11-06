typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef struct { void (*start)(void); u32 (*step)(void); void (*finish)(void); } Callbacks;

extern u8 data_ov003_021e0440[];
extern s8 data_ov003_021e0442[];
extern const Callbacks data_ov003_021e0104[];
extern void func_0206258c(u32);
extern void func_ov003_021d75c8(void);
extern void func_020407bc(u32);
extern void func_020c3a30(u32);
extern void func_020c40f4(u32);
extern void func_0205bf2c(u32);
extern void func_02041764(void);

u32 native_ov003_021d72d0(void) {
    const Callbacks *callbacks = data_ov003_021e0104 + ((s8 *)data_ov003_021e0440)[2];
    s8 *context = data_ov003_021e0442;
    u32 result = 12;
    switch (data_ov003_021e0440[1]) {
        case 0:
            callbacks->start();
            data_ov003_021e0440[1] = 1;
            break;
        case 1:
            if (callbacks->step()) {
                context[1] = context[0];
                data_ov003_021e0440[1] = 2;
            }
            break;
        case 2:
            callbacks->finish();
            if (context[2] == 1) {
                data_ov003_021e0440[1] = 4;
            } else if (context[2] == 2) {
                data_ov003_021e0440[1] = 3;
            }
            break;
        case 3:
            func_0206258c(0);
            result = 2;
            break;
        case 4:
            func_ov003_021d75c8();
            callbacks->finish();
            func_020407bc(1);
            func_020c3a30(1);
            func_020c40f4(1);
            func_0205bf2c(1);
            result = 1;
            break;
    }
    func_02041764();
    return result;
}
