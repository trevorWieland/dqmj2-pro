#ifndef ENCOUNTER_ACTOR_20261029
#define ENCOUNTER_ACTOR_20261029
typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef signed long long s64;
typedef float f32;
typedef struct { s32 v[9]; } Matrix33;
typedef struct { s32 v[3]; } Vector3;
typedef struct {
    u16 field0;
    u16 field2;
    u8 field4;
    u8 field5;
    u8 field6;
    u8 field7;
    u8 unknown8[10];
    u16 field12;
    u32 field14;
    u8 tail[20];
} FieldEnemy;
typedef struct {
    u8 prefix[0x16A];
    u16 field16a;
    u8 unknown16c[0x70];
    s8 sentinel1dc;
    u8 unknown1dd[0x8B];
    s8 array268[3];
    s8 array26b[3];
    s8 array26e[3];
    u8 unknown271[3];
    u8 active;
    u8 group;
    s16 enemy;
    u8 unknown278[12];
    Vector3 transformed;
    u8 unknown290[24];
    s32 x;
    s32 y;
    s32 z;
    s32 angle;
    s32 radius_squared;
    u32 field2bc;
    u8 field2c0;
    u8 field2c1;
    u8 field2c2;
    u8 field2c3;
} Actor;
typedef struct {
    u8 selector;
    u8 unknown1[15];
    s32 field10;
    s32 field14;
    s32 field18;
} ActorGlobal;
typedef char ActorSizeCheck[sizeof(Actor) == 0x2C4 ? 1 : -1];
typedef char FieldEnemySizeCheck[sizeof(FieldEnemy) == 44 ? 1 : -1];
#endif
