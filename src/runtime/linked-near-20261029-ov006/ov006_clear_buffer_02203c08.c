/* ov006 row 0x02203C08: 22 bytes.
 *
 * ov006_clear_buffer_02203c08: Obtains a buffer from 02203BD8 and clears size bytes of it.
 *
 * Evidence: Body: buffer = 02203BD8(); 02008D78(buffer, 0, size); return buffer. 02008D78 is the shared clear/fill primitive used elsewhere with a zero fill value.
 * Touches: buffer service 02203BD8; clear primitive 02008D78.
 * Remaining unknowns: The buffer's owner and lifetime are not established.
 *
 * The address stays in the symbol and file name because the measurement pairs a
 * compiled symbol to the private ledger row by its eight-hex address; removing
 * it would silently unmatch the row under the pinned private ledger.
 */
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
#define MULT_HI(a, b) ((s32)(((s64)(s32)(a) * (s32)(b)) >> 32))
#define MULTU_HI(a, b) ((u32)(((u64)(u32)(a) * (u32)(b)) >> 32))
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
extern u32 native_fn_02008d78();
extern u32 native_fn_ov006_02203bd8();
u32 ov006_clear_buffer_02203c08(u32 size) {
    u32 temp_r0;

    temp_r0 = native_fn_ov006_02203bd8();
    native_fn_02008d78(temp_r0, 0, size);
    return temp_r0;
}
