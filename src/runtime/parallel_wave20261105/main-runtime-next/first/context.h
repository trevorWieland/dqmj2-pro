typedef unsigned char u8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef struct MetadataFlags { u16 bits0:4; u16 nibble4:4; u16 bits8:8; } MetadataFlags;
typedef struct ItemMetadata { u8 opaque00[4]; MetadataFlags flags4; } ItemMetadata;
typedef struct TextContext { u8 opaque00[0x1e]; u8 style1e; u8 opaque1f[0x1d]; u8 state3c[0x22]; u8 format5e; u8 opaque5f[9]; void *field68; u16 field6c; } TextContext;
typedef struct TextOwner { u32 opaque00; TextContext *context04; } TextOwner;
extern ItemMetadata *native_fn_020449d4(u32);
extern void native_fn_02008be0(u32, void *, u32);
extern u32 native_fn_02087a48(TextContext *, u32, s16, s16, s32, u16 *);
extern void native_fn_020852b0(void *, u32);
extern void native_fn_02046af4(void *, const void *, u32, s32, u16 *, u32);
extern const u16 native_data_020dbc18[];
extern u8 native_data_021c9698[];
typedef char MetadataFlagsWidth[(sizeof(MetadataFlags) == 2) ? 1 : -1];
typedef char MetadataFlagsOffset[((u32)&((ItemMetadata *)0)->flags4 == 4) ? 1 : -1];
typedef char OwnerContextOffset[((u32)&((TextOwner *)0)->context04 == 4) ? 1 : -1];
typedef char TextStateOffset[((u32)&((TextContext *)0)->state3c == 0x3c) ? 1 : -1];
typedef char TextFormatOffset[((u32)&((TextContext *)0)->format5e == 0x5e) ? 1 : -1];
typedef char TextField68Offset[((u32)&((TextContext *)0)->field68 == 0x68) ? 1 : -1];
typedef struct Vec2 { s16 x; s16 y; } Vec2;
typedef struct EffectMetadata { u8 opaque00[0x24]; u8 symbol24; } EffectMetadata;
extern u32 native_fn_02060510(s32);
extern void native_fn_02085284(void *, u32, u32, u32);
extern u32 native_fn_020470fc(const u16 *);
extern EffectMetadata *native_fn_02065d88(u32);
extern u32 native_fn_02066a6c(u32);
static inline u16 advanceWidth(u16 current, u32 amount)
{
    return (u16)(current + amount);
}
extern void native_fn_02047ff0(const u8 *, u32, void *);
extern u32 native_fn_0203cfe0(void);
extern void native_fn_02044ff4(void *, s16, u32);
