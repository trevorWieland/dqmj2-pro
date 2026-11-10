/* Shared declarations for the ov000 low-address packet 3 (ov000-u1).
 *
 * Every symbol name carries its measured address and every record layout
 * carries only the field offsets the matched code proves; padding keeps the
 * byte counts exact. Mechanism comments live at their use sites in each source
 * file.
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

/* Three-word vector shared by the position builder and the renderer update. */
typedef struct {
    s32 x;
    s32 y;
    s32 z;
} Vec3;

/* Renderer state block returned by 0x021d8a44: the two vector mirrors the
   update keeps (0x1c/0x28 and 0x5c/0x68/0x74/0x80/0x8c), the published triple
   at 0x4c/0x50/0x54/0x58, and the last values at 0x98/0x9c/0xa0/0xa4. */
typedef struct {
    u8 pad_00[0x1c];
    Vec3 field_1c;
    Vec3 field_28;
    u8 pad_34[0x18];
    s32 field_4c;
    s32 field_50;
    s32 field_54;
    s32 field_58;
    Vec3 field_5c;
    Vec3 field_68;
    Vec3 field_74;
    Vec3 field_80;
    Vec3 field_8c;
    s32 field_98;
    s32 field_9c;
    s32 field_a0;
    s32 field_a4;
} StateBlock;

/* Task manager at 0x0223142c; 0x7c0 holds the current task id. */
typedef struct {
    u8 pad_00[0x7c0];
    u8 field_7c0;
} TaskManager;
extern TaskManager native_data_ov000_0223142c;

/* Task record template the task builder copies from. */
extern u8 native_data_ov000_0222e19c[];

/* Live task handle stored by the open helper. */
extern s32 native_data_ov000_022303e8;

extern StateBlock *native_fn_ov000_021d8a44();
extern u32 native_fn_02000ce8();
extern u32 native_fn_0200103c();
extern u32 native_fn_0201d444();
extern u32 native_fn_02027fe8();
extern u32 native_fn_02028044();
extern u32 native_fn_020280a0();
extern u32 native_fn_0202818c();
extern u32 native_fn_02028158();
extern u32 native_fn_02028dac();
extern u32 native_fn_0203cc2c();
extern u32 native_fn_ov000_021d84e8();
extern u32 native_fn_ov000_021d8a08();
extern u32 native_fn_ov000_021d8ae8();
extern u32 native_fn_ov000_021d8eb4();
extern u32 native_fn_ov000_021df220();
