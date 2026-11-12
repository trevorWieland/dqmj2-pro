/* ov001 row 0x0220f8b4: 104 bytes.
 *
 * What it does: 24 instructions; 3 call(s) to 0x0207b674, 0x0220f90c, 0x0203d294; loops (back edge at +0x14); returns through pop {r3, r4, r5, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 3 calls (24 instructions, 3 calls, 0 branches, 2 back edges, 2 literal slots).
 *
 *   pool +0x60 -> constant 0x66666667 (image word 0x66666667)
 *   pool +0x64 -> constant 0x51eb851f (image word 0x51eb851f)
 *   branch +0x1c -> +0x58
 *   test +0x18 cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220f8b4; the literal pool and
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

extern void native_fn_0207b674(void);
extern void native_fn_0203d294(void);


asm u32 native_ov001_0220f8b4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r1
    mov r1, r0
    mov r0, #14
    mov r4, #0
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_0220f8b4_L58
    mov r0, #11
    bl native_fn_0203d294
    add r2, r5, #5
    ldr r3, =0x66666667
    mov r1, r2, lsr #31
    smull r2, r12, r3, r2
    add r12, r1, r12, asr #2
    add r0, r0, #90
    mul r1, r12, r0
    ldr r2, =0x51eb851f
    mov r0, r1, lsr #31
    smull r1, r3, r2, r1
    add r3, r0, r3, asr #5
    add r4, r4, r3
ov001_0220f8b4_L58:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, pc}
}
