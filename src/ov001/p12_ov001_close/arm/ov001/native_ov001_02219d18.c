/* ov001 row 0x02219d18: 116 bytes.
 *
 * What it does: 28 instructions; 4 call(s) to 0x021db8d0, 0x021dbd30, 0x021dbcf0, +1 more; loops (back edge at +0x14); returns through pop {r4, r5, r6, r7, r8, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block load (28 instructions, 4 calls, 1 branch, 4 back edges, 1 literal slot).
 *
 *   pool +0x70 -> constant 0x66666667 (image word 0x66666667)
 *   branch +0x28 -> +0x58
 *   back edge +0x64 -> +0x10
 *   test +0x18 cmp r0, #0
 *   test +0x24 cmpne r1, r0
 *   test +0x4c cmp r4, r2
 *   test +0x5c cmp r6, #3
 *   1 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02219d18; the literal pool and
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

extern void native_fn_021db8d0(void);
extern void native_fn_021dbd30(void);
extern void native_fn_021dbcf0(void);


asm u32 native_ov001_02219d18 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    ldmia r0, {r5, r7}
    ldr r8, =0x66666667
    mov r6, #0
ov001_02219d18_L10:
    mov r0, r7
    bl native_fn_021db8d0
    cmp r0, #0
    ldrneb r1, [r5, #0x31f]
    ldrneb r0, [r7, #0x31f]
    cmpne r1, r0
    beq ov001_02219d18_L58
    mov r0, r7
    bl native_fn_021dbd30
    mov r4, r0
    mov r0, r7
    bl native_fn_021dbcf0
    smull r1, r2, r8, r0
    mov r0, r0, lsr #31
    add r2, r0, r2, asr #2
    cmp r4, r2
    movle r0, #1
    ldmleia sp!, {r4, r5, r6, r7, r8, pc}
ov001_02219d18_L58:
    add r6, r6, #1
    cmp r6, #3
    add r7, r7, #1088
    blt ov001_02219d18_L10
    mov r0, #0
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
