/* Shared declarations for the ov000 low-address packet (ov000-u1, packet 1).
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

/* Three-word parameter block copied between the actor and the controller.
   0x02230398 is the live block, 0x022303a4 the confirmed copy gameplay reads
   back, 0x022303b0 the pending copy. */
typedef struct {
    s32 word_0;
    s32 word_4;
    s32 word_8;
} ParameterBlock;

extern ParameterBlock native_data_ov000_02230398;
extern ParameterBlock native_data_ov000_022303a4;
extern ParameterBlock native_data_ov000_022303b0;

/* Controller counters at 0x022300c0: 00 counts live slots, 01 counts the bytes
   of the value list at 0x02230150 that the installer walks. */
typedef struct {
    u8 slot_count;
    u8 entry_count;
} ControllerCounts;
extern ControllerCounts native_data_ov000_022300c0;

/* Value list consumed by the per-entry installer at 0x0204861c. */
extern u8 native_data_ov000_02230150[];

/* Per-index selection table the two subsystem callbacks consume. */
extern u32 native_data_ov000_022300f8[];

/* Overlay controller state at 0x0223033c. 0x4c is the live value that
   0x021d84e8 swaps and 0x98 the value that swap recorded; 0x50 is the raw
   sample input, 0x54 an additive correction, 0x58 the animated offset that
   0x021d8a6c accumulates; 0x68/0x6c/0x70 are the three motion offsets that
   0x021d8378 folds into the resolved position at 0x74/0x78/0x7c. */
typedef struct {
    u8 pad_00[0x4c];
    s32 field_4c;
    s32 field_50;
    s32 field_54;
    s32 field_58;
    u8 pad_5c[0x0c];
    s32 field_68;
    s32 field_6c;
    s32 field_70;
    s32 field_74;
    s32 field_78;
    s32 field_7c;
    u8 pad_80[0x18];
    s32 field_98;
    s32 field_9c;
    s32 field_a0;
    s32 field_a4;
} ControllerState;
extern ControllerState native_data_ov000_0223033c;

/* Motion sample frame: the first helper fills it, the second seeds it with the
   live value, the third resolves the 0x24 and 0x30 sub-blocks. */
typedef struct {
    u8 pad_00[0x24];
    s32 field_24;
    s32 field_28;
    s32 field_2c;
    s32 field_30;
    s32 field_34;
    s32 field_38;
} SampleFrame;

/* Actor block shared by the install-time helpers. 0x1e8/0x1f4/0x200 hold the
   three confirmed parameter blocks, 0x20c the install selection, 0x264 the
   optional completion callback. */
typedef struct {
    u8 pad_00[0x1e8];
    ParameterBlock field_1e8;
    ParameterBlock field_1f4;
    ParameterBlock field_200;
    s32 field_20c;
    u8 pad_210[0x54];
    u32 field_264;
} Actor;

/* Per-slot one-byte state; negative means the slot is already released. */
extern s8 native_data_ov000_022322d0[];

/* Phase byte at 0x0223254c, addressed through its measured base symbol. */
typedef struct {
    u8 pad_00[0x278];
    u8 field_278;
} PhaseState;
extern PhaseState native_data_ov000_022322d4;

/* Archive slot identity handed to the layout service. */
extern u8 native_data_ov000_0222ebd8;

extern u32 native_fn_02000ce8();
extern u32 native_fn_0200103c();
extern u32 native_fn_0200285c();
extern u32 native_fn_02028158();
extern u32 native_fn_020404e0();
extern u32 native_fn_0204861c();
extern u32 native_fn_02049ffc();
extern u32 native_fn_0205bfd4();
extern u32 native_fn_0205ce38();
extern u32 native_fn_0205d718();
extern u32 native_fn_02087a48();
extern u32 native_fn_ov000_021d7d90();
extern u32 native_fn_ov000_021e0654();
extern u32 native_fn_ov000_021e87d4();
extern u32 native_fn_ov000_02210758();
