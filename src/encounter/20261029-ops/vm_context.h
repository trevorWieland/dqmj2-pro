#ifndef ENCOUNTER_VM_OPS_20261029
#define ENCOUNTER_VM_OPS_20261029
typedef unsigned char u8;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef float f32;
typedef union { f32 number; u32 bits; } NativeValue;
typedef struct {
    u32 pc;
    s16 depth;
    u8 active;
    u8 pending;
    u8 wait_phase;
    u8 unknown9;
    s16 wait_count;
    u32 return_pc[64];
} NativeVmThread;
typedef struct {
    u8 active;
    u8 running;
    u8 condition;
    u8 thread;
    u32 entry;
    const void *source;
    const void *code;
    NativeValue arguments[16];
    NativeValue variables[256];
    NativeValue context[8];
    NativeVmThread threads[4];
} NativeVm;
typedef struct {
    u32 opcode;
    u32 bytes;
    u32 destination_type;
    f32 destination_value;
    u32 left_type;
    f32 left_value;
    u32 right_type;
    f32 right_value;
} NativeInstruction;
typedef char NativeVmSizeCheck[sizeof(NativeVm) == 0x8a0 ? 1 : -1];
typedef char NativeVmThreadSizeCheck[sizeof(NativeVmThread) == 0x10c ? 1 : -1];
#endif
