/* Shared declarations for the ov006 layout-switch packet (ov006-u1).
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

/* Layout block at 0x0220f33c; 0x08 holds the current layout buffer. */
typedef struct {
    u8 pad_00[0x08];
    u8 *field_08;
} LayoutBlock;
extern LayoutBlock native_data_ov006_0220f33c;

/* Dispatch block at 0x02219290: 0x14 is the dispatch state and 0x1c the table
   entry index handed to 0x021eba54. */
typedef struct {
    u8 pad_00[0x14];
    s32 field_14;
    u8 pad_18[0x04];
    s32 field_1c;
} DispatchBlock;
extern DispatchBlock native_data_ov006_02219290;

/* Dispatch table base the index selects a 12-byte entry from. */
extern u8 native_data_ov006_022087e4[];

/* Display registers the layout switch reprograms. */
extern u32 native_data_04000000;
extern u16 native_data_0400000e;
extern u32 native_data_0400001c;

extern u32 native_fn_02004d98();
extern u32 native_fn_020bb38c();
extern u32 native_fn_ov006_021da3e8();
extern u32 native_fn_ov006_022078bc(s8, u8, s32, s16, s32);
