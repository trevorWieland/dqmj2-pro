#ifndef ENCOUNTER_VM_CONTEXT_20261029
#define ENCOUNTER_VM_CONTEXT_20261029
typedef unsigned char u8;
typedef signed short s16;
typedef unsigned int u32;
typedef float f32;
typedef struct {
    u32 pc;
    u8 status[3];
    u8 pending;
    u8 remaining[0x104];
} NativeVmThread;
typedef struct {
    u8 active;
    u8 running;
    u8 condition;
    u8 thread;
    u32 entry;
    const void *source;
    const void *code;
    f32 arguments[16];
    f32 variables[256];
    f32 context[8];
    NativeVmThread threads[4];
} NativeVm;
typedef struct {
    u32 opcode;
    u32 bytes;
    u32 left_type;
    f32 left_value;
    u32 right_type;
    f32 right_value;
} NativeInstruction;
typedef char NativeVmSizeCheck[sizeof(NativeVm) == 0x8a0 ? 1 : -1];
typedef char NativeVmThreadSizeCheck[sizeof(NativeVmThread) == 0x10c ? 1 : -1];
#endif
