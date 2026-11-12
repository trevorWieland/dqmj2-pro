/* ov001 row 0x022244a0: 208 bytes.
 *
 * What it does: 51 instructions; 11 call(s) to 0x021dbd24, 0x021dbd30, 0x021dbcbc, +8 more; loops (back edge at +0x3c); returns through pop {r4, r5, r6, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 11 calls (51 instructions, 11 calls, 11 branches, 11 back edges, 1 literal slot).
 *
 *   pool +0xcc -> constant 0x51eb851f (image word 0x51eb851f)
 *   branch +0x10 -> +0xc4
 *   branch +0x14 -> +0x3c
 *   branch +0x18 -> +0x44
 *   branch +0x1c -> +0x4c
 *   branch +0x20 -> +0x54
 *   branch +0x24 -> +0x5c
 *   branch +0x28 -> +0x64
 *   branch +0x2c -> +0x6c
 *   branch +0x30 -> +0x74
 *   branch +0x34 -> +0xc4
 *   branch +0x38 -> +0x7c
 *   test +0x08 cmp r1, #9
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022244a0; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_021dbd24(void);
extern void native_fn_021dbd30(void);
extern void native_fn_021dbcbc(void);
extern void native_fn_021dbcf0(void);
extern void native_fn_021dbd3c(void);
extern void native_fn_021dbd8c(void);
extern void native_fn_021dbe5c(void);
extern void native_fn_021dbe68(void);
extern void native_fn_021ef02c(void);


asm u32 native_ov001_022244a0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r6, r0
    cmp r1, #9
    addls pc, pc, r1, lsl #2
    b ov001_022244a0_Lc4
    b ov001_022244a0_L3c
    b ov001_022244a0_L44
    b ov001_022244a0_L4c
    b ov001_022244a0_L54
    b ov001_022244a0_L5c
    b ov001_022244a0_L64
    b ov001_022244a0_L6c
    b ov001_022244a0_L74
    b ov001_022244a0_Lc4
    b ov001_022244a0_L7c
ov001_022244a0_L3c:
    bl native_fn_021dbd24
    ldmia sp!, {r4, r5, r6, pc}
ov001_022244a0_L44:
    bl native_fn_021dbd30
    ldmia sp!, {r4, r5, r6, pc}
ov001_022244a0_L4c:
    bl native_fn_021dbcbc
    ldmia sp!, {r4, r5, r6, pc}
ov001_022244a0_L54:
    bl native_fn_021dbcf0
    ldmia sp!, {r4, r5, r6, pc}
ov001_022244a0_L5c:
    bl native_fn_021dbd3c
    ldmia sp!, {r4, r5, r6, pc}
ov001_022244a0_L64:
    bl native_fn_021dbd8c
    ldmia sp!, {r4, r5, r6, pc}
ov001_022244a0_L6c:
    bl native_fn_021dbe5c
    ldmia sp!, {r4, r5, r6, pc}
ov001_022244a0_L74:
    bl native_fn_021dbe68
    ldmia sp!, {r4, r5, r6, pc}
ov001_022244a0_L7c:
    bl native_fn_021dbd3c
    mov r4, r0
    mov r0, r6
    bl native_fn_021dbd3c
    mov r5, r0
    mov r0, r6
    mov r1, #0
    mov r2, #100
    bl native_fn_021ef02c
    mul r1, r5, r0
    ldr r2, =0x51eb851f
    mov r0, r1, lsr #31
    smull r1, r3, r2, r1
    add r3, r0, r3, asr #5
    mov r0, r3, asr #1
    add r0, r3, r0, lsr #30
    add r0, r4, r0, asr #2
    ldmia sp!, {r4, r5, r6, pc}
ov001_022244a0_Lc4:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, pc}
}
