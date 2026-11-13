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
extern u32 native_fn_01ffa02c();
extern u32 native_fn_01ffa050();
extern u32 native_fn_020841c4();
extern u32 native_fn_020844fc();
extern u32 ov000_context_02246600_02223c54();
extern u32 native_data_021cebe0;
void native_itcm_01ffa2a4(s16 arg0) {
    native_fn_01ffa050();
    if ((arg0 == 0x10) && (M2C_FIELD((void *) ov000_context_02246600_02223c54(), s8 *, 0x59) == 1)) {
        native_fn_020844fc(0x1223);
    }
    native_fn_020841c4();
    *(s16 *) native_fn_01ffa02c() = arg0;
    M2C_FIELD(&native_data_021cebe0, s16 *, 0x7C) = arg0;
    if (arg0 == 0x10) {
        M2C_FIELD(&native_data_021cebe0, s16 *, 0x7E) = 1;
    }
}
