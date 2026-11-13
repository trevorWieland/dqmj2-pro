/* ov001 row 0x0221efd4: 208 bytes.
 *
 * What it does: 51 instructions; 8 call(s) to 0x021dbe5c, 0x021db8d0, 0x021dbe5c, +5 more; loops (back edge at +0x14); returns through pop {r4, r5, r6, r7, r8, r9, r10, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block load (51 instructions, 8 calls, 5 branches, 7 back edges, 1 literal slot).
 *
 *   pool +0xcc -> constant 0x66666667 (image word 0x66666667)
 *   branch +0x2c -> +0x50
 *   branch +0x3c -> +0x50
 *   branch +0x4c -> +0x68
 *   back edge +0x64 -> +0x24
 *   branch +0x6c -> +0xc4
 *   branch +0x94 -> +0xa8
 *   branch +0xa4 -> +0xc4
 *   back edge +0xc0 -> +0x88
 *   test +0x28 cmp r5, r0
 *   test +0x38 cmp r0, #0
 *   test +0x48 cmp r0, r6
 *   test +0x50 cmp r5, #2
 *   test +0x5c cmp r5, #3
 *   test +0x68 cmp r7, #0
 *   test +0x90 cmp r0, #0
 *   test +0xa0 cmp r0, r4
 *   test +0xa8 cmp r5, #2
 *   test +0xb8 cmp r5, #3
 *   1 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221efd4; the literal pool and
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

extern void native_fn_021dbe5c(void);
extern void ov001_record_is_active_021db8d0(void);


asm u32 native_ov001_0221efd4 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    ldmia r0, {r4, r9}
    ldr r8, [r0, #0x8]
    mov r0, r4
    mov r7, #0
    bl native_fn_021dbe5c
    mov r6, r0
    mov r5, r7
    mov r10, #1
ov001_0221efd4_L24:
    ldrb r0, [r4, #0x31f]
    cmp r5, r0
    beq ov001_0221efd4_L50
    mov r0, r9
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_0221efd4_L50
    mov r0, r9
    bl native_fn_021dbe5c
    cmp r0, r6
    blt ov001_0221efd4_L68
ov001_0221efd4_L50:
    cmp r5, #2
    add r5, r5, #1
    moveq r7, r10
    cmp r5, #3
    add r9, r9, #1088
    blt ov001_0221efd4_L24
ov001_0221efd4_L68:
    cmp r7, #0
    beq ov001_0221efd4_Lc4
    ldr r1, =0x66666667
    mov r2, r6, lsl #2
    smull r0, r4, r1, r2
    mov r0, r2, lsr #31
    add r4, r0, r4, asr #2
    mov r5, #0
ov001_0221efd4_L88:
    mov r0, r8
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_0221efd4_La8
    mov r0, r8
    bl native_fn_021dbe5c
    cmp r0, r4
    bgt ov001_0221efd4_Lc4
ov001_0221efd4_La8:
    cmp r5, #2
    moveq r0, #1
    ldmeqia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
    add r5, r5, #1
    cmp r5, #3
    add r8, r8, #1088
    blt ov001_0221efd4_L88
ov001_0221efd4_Lc4:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
