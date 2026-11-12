/* ov001 row 0x021e215c: 284 bytes.
 *
 * What it does: 70 instructions; 8 call(s) to 0x021db438, 0x021db8d0, 0x021e1f5c, +5 more; loops (back edge at +0x28); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 8 calls (70 instructions, 8 calls, 5 branches, 8 back edges, 1 literal slot).
 *
 *   pool +0x118 -> constant 0x022388ec (image word 0x022388ec)
 *   branch +0x54 -> +0xd8
 *   branch +0x84 -> +0xd8
 *   branch +0x90 -> +0xa0
 *   branch +0x9c -> +0xbc
 *   branch +0xb8 -> +0xd8
 *   back edge +0xe4 -> +0x48
 *   test +0x18 cmp r0, #0
 *   test +0x50 cmp r0, #0
 *   test +0x80 cmp r0, #2
 *   test +0x8c cmp r0, #0
 *   test +0x98 cmp r0, #0
 *   test +0xdc cmp r8, #3
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e215c; the literal pool and
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

extern void native_fn_021db438(void);
extern void native_fn_021db8d0(void);
extern void native_fn_021e1f5c(void);
extern void native_fn_020449d4(void);
extern void native_fn_020444a8(void);
extern void native_fn_021e1f74(void);


asm u32 native_ov001_021e215c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #12
    mov r1, #0
    str r1, [sp, #0x8]
    str r1, [sp, #0x4]
    ldrb r0, [r0, #0x31e]
    cmp r0, #0
    moveq r1, #1
    mov r0, r1
    mov r1, #0
    bl native_fn_021db438
    mov r4, #2
    mov r10, r0
    mov r8, #0
    add r6, sp, #8
    add r5, sp, #4
    mov r7, r4
    mov r11, #20
ov001_021e215c_L48:
    mov r0, r10
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_021e215c_Ld8
    mov r0, r10
    bl native_fn_021e1f5c
    ldr r1, [r10, #0x1e8]
    mov r9, r0
    ldrsh r0, [r1, #42]
    bl native_fn_020449d4
    ldrh r0, [r0, #4]
    mov r0, r0, lsl #24
    mov r0, r0, lsr #28
    and r0, r0, #255
    cmp r0, #2
    bne ov001_021e215c_Ld8
    ldrb r0, [r10, #0x31e]
    cmp r0, #0
    beq ov001_021e215c_La0
    bl native_fn_020444a8
    cmp r0, #0
    beq ov001_021e215c_Lbc
ov001_021e215c_La0:
    mul r1, r9, r11
    mov r0, r10
    mov r2, r6
    mov r3, r5
    str r7, [sp]
    bl native_fn_021e1f74
    b ov001_021e215c_Ld8
ov001_021e215c_Lbc:
    mov r0, #10
    mul r1, r9, r0
    mov r0, r10
    mov r2, r6
    mov r3, r5
    str r4, [sp]
    bl native_fn_021e1f74
ov001_021e215c_Ld8:
    add r8, r8, #1
    cmp r8, #3
    add r10, r10, #1088
    blt ov001_021e215c_L48
    ldr r1, =0x022388ec
    ldr r4, [sp, #0x8]
    ldrb r0, [r1, #0x18]
    ldr r3, [sp, #0x4]
    add r0, r0, r4
    strb r0, [r1, #0x18]
    ldrb r2, [r1, #0x19]
    add r0, r4, r3
    add r2, r2, r3
    strb r2, [r1, #0x19]
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
