/* ov001 row 0x0221f98c: 148 bytes.
 *
 * What it does: 36 instructions; 7 call(s) to 0x021db8d0, 0x021dbe5c, 0x021dbe5c, +4 more; loops (back edge at +0x18); returns through pop {r4, r5, r6, r7, r8, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 7 calls (36 instructions, 7 calls, 1 branch, 6 back edges, 1 literal slot).
 *
 *   pool +0x90 -> constant 0x66666667 (image word 0x66666667)
 *   branch +0x20 -> +0x78
 *   branch +0x44 -> +0x78
 *   back edge +0x84 -> +0x14
 *   test +0x1c cmp r0, #0
 *   test +0x40 cmp r4, r0, asr #1
 *   test +0x6c cmp r4, r2
 *   test +0x7c cmp r6, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221f98c; the literal pool and
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

extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021dbe5c(void);
extern void native_fn_021dbd24(void);


asm u32 native_ov001_0221f98c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    ldr r5, [r0]
    ldr r7, [r0, #0x8]
    ldr r8, =0x66666667
    mov r6, #0
ov001_0221f98c_L14:
    mov r0, r7
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_0221f98c_L78
    mov r0, r5
    bl native_fn_021dbe5c
    mov r4, r0
    mov r0, r7
    bl native_fn_021dbe5c
    add r0, r0, r0, lsl #1
    add r0, r0, r0, lsr #31
    cmp r4, r0, asr #1
    blt ov001_0221f98c_L78
    mov r0, r7
    bl native_fn_021dbd24
    mov r4, r0
    mov r0, r5
    bl native_fn_021dbd24
    add r1, r0, r0, lsl #1
    smull r0, r2, r8, r1
    mov r0, r1, lsr #31
    add r2, r0, r2, asr #2
    cmp r4, r2
    movle r0, #1
    ldmleia sp!, {r4, r5, r6, r7, r8, pc}
ov001_0221f98c_L78:
    add r6, r6, #1
    cmp r6, #3
    add r7, r7, #1088
    blt ov001_0221f98c_L14
    mov r0, #0
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
