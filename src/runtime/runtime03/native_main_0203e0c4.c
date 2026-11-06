typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
typedef float f32;
typedef double f64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_fn_0203dd48();
extern u32 native_fn_0203dee8();
extern u32 native_fn_0203fe08();
extern u32 native_fn_02040434();
extern u32 native_fn_02040554();
extern u32 native_fn_0204070c();
extern u32 native_fn_ov000_021d8ccc();
extern u32 native_fn_ov000_021e1894();
extern u32 native_fn_ov000_021e3068();
extern u32 native_fn_ov000_021e6278();
extern u32 native_fn_ov000_02219e04();
u32 native_main_0203e0c4(void) {
    if (native_fn_0204070c() != 0) {
        native_fn_0203dee8();
        native_fn_ov000_021e1894(0);
        native_fn_0203dd48();
        native_fn_02040434();
    } else {
        native_fn_0203fe08();
        native_fn_02040554();
        native_fn_ov000_021e6278();
        native_fn_ov000_021e3068();
        native_fn_0203dd48();
        native_fn_ov000_021d8ccc(-1, -1, -0x1000);
        native_fn_02040434();
        native_fn_ov000_02219e04();
    }
    return 0U;
}
