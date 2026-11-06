#ifndef PRIVATE_ANIMATION_TYPES_V2_20261030
#define PRIVATE_ANIMATION_TYPES_V2_20261030
typedef unsigned char u8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef struct AnimationFrame {
    void *content;
    u16 duration;
    u16 pad;
} AnimationFrame;
typedef struct AnimationSequence {
    u16 count;
    u16 loopStart;
    u32 type;
    u32 mode;
    AnimationFrame *frames;
} AnimationSequence;
typedef struct AnimationControl {
    AnimationFrame *frame;
    AnimationFrame *active;
    u32 reverse;
    u32 running;
    s32 elapsed;
    s32 speed;
    u32 pad;
    AnimationSequence *sequence;
    u32 callbackMode;
    u32 callbackUser;
    u32 callbackFunction;
    u16 callbackFlags;
    u16 callbackPad;
} AnimationControl;
typedef struct CellBank {
    u16 count;
    u16 flags;
    void *cells;
    u32 pad;
    void *extension;
} CellBank;
typedef struct CellAnimation {
    AnimationControl control;
    void *cell;
    CellBank *bank;
    u32 index;
    u8 transform[0x1C];
} CellAnimation;
#endif
