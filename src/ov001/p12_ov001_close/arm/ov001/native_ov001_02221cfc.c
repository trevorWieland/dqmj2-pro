/* ov001 row 0x02221cfc: 104 bytes.
 *
 * What it does: 25 instructions; 4 call(s) to 0x021db8d0, 0x021dbd24, 0x021dbcbc, +1 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 4 calls (25 instructions, 4 calls, 1 branch, 4 back edges, 1 literal slot).
 *
 *   pool +0x64 -> constant 0x66666667 (image word 0x66666667)
 *   branch +0x1c -> +0x4c
 *   back edge +0x58 -> +0x10
 *   test +0x18 cmp r0, #0
 *   test +0x40 cmp r5, r2
 *   test +0x50 cmp r6, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02221cfc; the literal pool and
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
extern void native_fn_021dbd24(void);
extern void native_fn_021dbcbc(void);


asm u32 native_ov001_02221cfc (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    ldr r7, [r0, #0x8]
    ldr r4, =0x66666667
    mov r6, #0
ov001_02221cfc_L10:
    mov r0, r7
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_02221cfc_L4c
    mov r0, r7
    bl native_fn_021dbd24
    mov r5, r0
    mov r0, r7
    bl native_fn_021dbcbc
    smull r1, r2, r4, r0
    mov r0, r0, lsr #31
    add r2, r0, r2, asr #2
    cmp r5, r2
    movle r0, #1
    ldmleia sp!, {r3, r4, r5, r6, r7, pc}
ov001_02221cfc_L4c:
    add r6, r6, #1
    cmp r6, #3
    add r7, r7, #1088
    blt ov001_02221cfc_L10
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
