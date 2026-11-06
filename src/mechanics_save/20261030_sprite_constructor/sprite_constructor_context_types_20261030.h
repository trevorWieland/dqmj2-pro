#ifndef PRIVATE_SPRITE_CONSTRUCTOR_TYPES_20261030
#define PRIVATE_SPRITE_CONSTRUCTOR_TYPES_20261030
#include "../20261030_state_writer/state_writer_types_20261030.h"
typedef struct ResourceCounters {
    s8 slots;
    s8 children;
    u8 loaded;
    u8 unknown3;
    s16 tiles;
    unsigned short unknown6;
} ResourceCounters;
typedef struct SpriteSlot {
    u8 unknown0;
    u8 children;
    s8 first;
    u8 kind;
    u32 resource;
    s8 marker;
    u8 unknown9;
    s16 species;
    u8 form;
    u8 remaining[11];
} SpriteSlot;
typedef struct SpriteResources {
    ResourceCounters counters;
    u32 childObjects[30];
    u32 mainObjects[15];
    u8 resourceObject[72];
    SpriteSlot slots[15];
} SpriteResources;
extern SpriteResources native_data_021c4af4;
extern u32 native_fn_02044cdc(s32);
extern void native_fn_0206d2e0(s32, s32, u32, u32, s32, s8, u32);
#endif
