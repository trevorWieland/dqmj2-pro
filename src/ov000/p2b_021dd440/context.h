/* Shared declarations for the ov000 low-address packet 2 (ov000-u1).
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

/* Three-word parameter block copied between the actor and the controller. */
typedef struct {
    s32 word_0;
    s32 word_4;
    s32 word_8;
} ParameterBlock;

/* 20-byte payload records copied into the slot blocks below. */
typedef struct {
    u32 words[5];
} Payload20;

/* Slot block entry: the owning index word followed by the 20-byte payload. The
   index array and the payload array are addressed through their own measured
   symbols and share the 0x18-byte stride. */
typedef struct {
    s32 index;
    u8 pad_04[0x14];
} Slot24;
typedef struct {
    u32 words[5];
    u8 pad_14[0x04];
} Payload24;

/* Pointer table selecting which source array each register function drains. */
extern Payload20 *native_data_ov000_02231bf0[];

extern Slot24 native_data_ov000_02231e44[];
extern Payload24 native_data_ov000_02231e48[];
extern Slot24 native_data_ov000_02231c04[];
extern Payload24 native_data_ov000_02231c08[];
extern Slot24 native_data_ov000_02231d24[];
extern Payload24 native_data_ov000_02231d28[];

/* Four-slot window block cleared and walked by 0x021dfe0c. */
extern u8 native_data_ov000_02232264[];

/* Display register at 0x04000060 (16-bit). */
extern u16 native_data_04000060;

/* Device block reached through the manager's 0x79c pointer. */
typedef struct {
    u8 pad_00[0x190];
    s32 field_190;
} DeviceBlock;
typedef struct {
    u8 pad_00[0x79c];
    DeviceBlock *field_79c;
} DeviceManager;
extern DeviceManager native_data_ov000_0223142c;

extern u32 native_fn_02008c58();
extern u32 native_fn_020286e8(void *, u8);
extern u32 native_fn_020298a8();
extern u32 native_fn_02029d84();
extern u32 native_fn_0203caa4();
extern u32 native_fn_0203cac8();
extern u32 native_fn_ov000_021dd1e4();
extern u32 native_fn_ov000_021dd2a4();
extern u32 native_fn_ov000_021df5f0();
extern u32 native_fn_ov000_021df624();
extern u32 native_fn_ov000_021df69c();
extern u32 native_fn_ov000_021df6d0();
extern u32 native_fn_ov000_021df748();
extern u32 native_fn_ov000_021df77c();
extern u32 native_fn_ov000_021dfea4(s32, s32);
