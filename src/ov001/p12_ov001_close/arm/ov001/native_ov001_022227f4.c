/* ov001 row 0x022227f4: 252 bytes.
 *
 * What it does: 62 instructions; 10 call(s) to 0x021db8d0, 0x02218644, 0x021db8d0, +7 more; loops (back edge at +0x20); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 10 calls (62 instructions, 10 calls, 4 branches, 10 back edges, 1 literal slot).
 *
 *   pool +0xf8 -> constant 0x66666667 (image word 0x66666667)
 *   branch +0x28 -> +0xe0
 *   branch +0x3c -> +0xe0
 *   branch +0x58 -> +0xc8
 *   branch +0x70 -> +0xb8
 *   back edge +0xc4 -> +0x64
 *   back edge +0xd4 -> +0x4c
 *   back edge +0xec -> +0x1c
 *   test +0x24 cmp r0, #0
 *   test +0x38 cmp r0, #0
 *   test +0x54 cmp r0, #0
 *   test +0x6c cmp r0, #0
 *   test +0xac cmp r3, r2
 *   test +0xbc cmp r8, #3
 *   test +0xcc cmp r11, #3
 *   test +0xe4 cmp r5, #3
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022227f4; the literal pool and
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
extern void native_fn_02218644(void);
extern void native_fn_021dbd24(void);
extern void native_fn_02218c34(void);
extern void native_fn_021dbcbc(void);


asm u32 native_ov001_022227f4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    ldr r1, [r0, #0x8]
    ldr r9, [r0, #0x4]
    str r1, [sp]
    mov r6, r1
    mov r5, #0
    mov r4, #43
ov001_022227f4_L1c:
    mov r0, r6
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_022227f4_Le0
    mov r0, r6
    mov r1, r4
    bl native_fn_02218644
    cmp r0, #0
    beq ov001_022227f4_Le0
    mov r11, #0
    ldr r4, =0x66666667
    mov r6, r11
ov001_022227f4_L4c:
    mov r0, r9
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_022227f4_Lc8
    ldr r10, [sp]
    mov r8, #0
ov001_022227f4_L64:
    mov r0, r10
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_022227f4_Lb8
    mov r0, r10
    bl native_fn_021dbd24
    mov r7, r0
    mov r0, r9
    mov r1, r10
    mov r2, r6
    bl native_fn_02218c34
    mov r5, r0
    mov r0, r10
    bl native_fn_021dbcbc
    smull r1, r2, r4, r0
    mov r0, r0, lsr #31
    sub r3, r7, r5
    add r2, r0, r2, asr #1
    cmp r3, r2
    movle r0, #1
    ldmleia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_022227f4_Lb8:
    add r8, r8, #1
    cmp r8, #3
    add r10, r10, #1088
    blt ov001_022227f4_L64
ov001_022227f4_Lc8:
    add r11, r11, #1
    cmp r11, #3
    add r9, r9, #1088
    blt ov001_022227f4_L4c
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_022227f4_Le0:
    add r5, r5, #1
    cmp r5, #3
    add r6, r6, #1088
    blt ov001_022227f4_L1c
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
