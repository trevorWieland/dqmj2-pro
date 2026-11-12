/* ov006 row 0x021dc178: 236 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xe8 -> native_data2_0220f3b8 (image word 0x0220f3b8)
 *   branch +0x48 -> +0xc0
 *   branch +0x5c -> +0x90
 *   branch +0x8c -> +0xd8
 *   branch +0xbc -> +0xd8
 *   back edge +0xe0 -> +0x38
 *   test +0x44 cmp r0, #1
 *   test +0x54 cmp r0, #0
 *   test +0xdc cmp r5, #8
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021dc178; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data2_0220f3b8[];
extern void native_fn_021d79e4(void);
extern void native_fn_02067a7c(void);
extern void native_fn_021dc278(void);
extern void native_fn_021d7c1c(void);
extern void native_fn_021dc28c(void);


asm u32 native_ov006_021dc178 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    ldr r1, =native_data2_0220f3b8
    mov r0, #0
    ldr r2, [r1, #0x8]
    mov r1, #15
    add r2, r2, #89
    and r3, r2, #255
    mov r2, #2
    bl native_fn_021d79e4
    ldr r6, =native_data2_0220f3b8
    mov r5, #0
    mov r9, #15
    mov r8, #2
    mov r7, #122
ov006_021dc178_L38:
    ldr r0, [r6, #0x10]
    add r0, r0, #8
    bl native_fn_02067a7c
    cmp r0, #1
    bne ov006_021dc178_Lc0
    ldr r0, [r6, #0x8]
    mov r1, r5
    cmp r0, #0
    ldr r0, [r6, #0x10]
    bne ov006_021dc178_L90
    bl native_fn_021dc278
    mov r4, r0
    ldr r0, [r6, #0x10]
    mov r1, r5
    bl native_fn_021dc278
    mov r2, r0
    add r0, r5, #9
    ldrh r1, [r4]
    ldrb r2, [r2, #0x2]
    and r0, r0, #255
    bl native_fn_021d7c1c
    b ov006_021dc178_Ld8
ov006_021dc178_L90:
    bl native_fn_021dc28c
    mov r4, r0
    ldr r0, [r6, #0x10]
    mov r1, r5
    bl native_fn_021dc28c
    mov r2, r0
    add r0, r5, #9
    ldrh r1, [r4]
    ldrb r2, [r2, #0x2]
    and r0, r0, #255
    bl native_fn_021d7c1c
    b ov006_021dc178_Ld8
ov006_021dc178_Lc0:
    add r0, r5, #9
    mov r1, r9
    mov r2, r8
    mov r3, r7
    and r0, r0, #255
    bl native_fn_021d79e4
ov006_021dc178_Ld8:
    add r5, r5, #1
    cmp r5, #8
    blt ov006_021dc178_L38
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
