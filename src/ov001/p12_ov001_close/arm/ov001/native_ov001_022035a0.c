/* ov001 row 0x022035a0: 112 bytes.
 *
 * What it does: 28 instructions; 4 call(s) to 0x021db4b4, 0x021db4b4, 0x021db8d0, +1 more; loops (back edge at +0x28); returns through pop {r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: loop with 4 calls (28 instructions, 4 calls, 4 branches, 4 back edges, 0 literal slots).
 *
 *   branch +0x20 -> +0x58
 *   branch +0x30 -> +0x48
 *   branch +0x44 -> +0x58
 *   branch +0x54 -> +0x68
 *   back edge +0x64 -> +0x18
 *   test +0x1c cmp r1, #0
 *   test +0x2c cmp r0, #0
 *   test +0x40 cmp r0, #0
 *   test +0x4c cmp r0, #0
 *   test +0x60 cmp r7, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022035a0; the literal pool and
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

extern void native_fn_021db4b4(void);
extern void ov001_record_is_active_021db8d0(void);


asm u32 native_ov001_022035a0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    mov r6, #0
    mov r8, r0
    mov r7, r6
    mov r5, r6
    mov r4, #2
ov001_022035a0_L18:
    ldr r1, [r8, r7, lsl #2]
    cmp r1, #0
    beq ov001_022035a0_L58
    mov r0, r5
    bl native_fn_021db4b4
    cmp r0, #0
    bne ov001_022035a0_L48
    ldr r1, [r8, r7, lsl #2]
    mov r0, r4
    bl native_fn_021db4b4
    cmp r0, #0
    beq ov001_022035a0_L58
ov001_022035a0_L48:
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    movne r6, #1
    bne ov001_022035a0_L68
ov001_022035a0_L58:
    add r0, r7, #1
    and r7, r0, #255
    cmp r7, #3
    blo ov001_022035a0_L18
ov001_022035a0_L68:
    mov r0, r6
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
