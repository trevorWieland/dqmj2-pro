/* ov006 row 0x021ffbc4: 132 bytes.
 *
 * What it does: Writes one block of 2 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x78 -> native_data3_0221c150 (image word 0x0221c150)
 *   pool +0x7c -> native_data2_0220ba1e (image word 0x0220ba1e)
 *   pool +0x80 -> native_fn_021ffc48+1 (image word 0x021ffc49)
 *   branch +0x1e -> +0x46
 *   back edge +0x40 -> +0x28
 *   back edge +0x6a -> +0x52
 *   test +0x1c cmp r0, #0x68
 *   test +0x3e cmp r6, #0x5
 *   test +0x68 cmp r6, #0x5
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ffbc4; the literal pool and
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

extern u8 native_data3_0221c150[];
extern void native_fn_02202f98(void);
extern u8 native_data2_0220ba1e[];
extern void native_fn_02202eb0(void);
extern void native_fn_021ffc48(void);
extern void native_fn_02204970(void);


asm u32 native_ov006_021ffbc4 (register u32 a0)
{
    push {r4, r5, r6, r7, lr}
    sub sp, #0xc
    str r0, [sp]
    ldr r0, =native_data3_0221c150
    mov r1, #0x0
    ldr r0, [r0, #0x4]
    add r2, sp, #0x8
    ldr r0, [r0, #0xc]
    add r3, sp, #0x4
    bl native_fn_02202f98
    ldr r0, [sp, #0x8]
    sub r0, #0x8
    str r0, [sp, #0x8]
    cmp r0, #0x68
    ble ov006_021ffbc4_L46
    ldr r4, =native_data2_0220ba1e
    ldr r7, =native_data3_0221c150
    mov r6, #0x3
    mov r5, #0xc
ov006_021ffbc4_L28:
    ldr r0, [r7, #0x4]
    ldrh r3, [r4, #0x2]
    mov r1, #0x0
    ldr r0, [r0, r5]
    ldr r2, [sp, #0x8]
    mvn r1, r1
    bl native_fn_02202eb0
    add r6, r6, #0x1
    add r4, r4, #0x4
    add r5, r5, #0x4
    cmp r6, #0x5
    blt ov006_021ffbc4_L28
    add sp, #0xc
    pop {r4, r5, r6, r7, pc}
ov006_021ffbc4_L46:
    mov r0, #0x68
    ldr r4, =native_data2_0220ba1e
    ldr r7, =native_data3_0221c150
    str r0, [sp, #0x8]
    mov r6, #0x3
    mov r5, #0xc
ov006_021ffbc4_L52:
    ldr r0, [r7, #0x4]
    ldrh r3, [r4, #0x2]
    mov r1, #0x0
    ldr r0, [r0, r5]
    ldr r2, [sp, #0x8]
    mvn r1, r1
    bl native_fn_02202eb0
    add r6, r6, #0x1
    add r4, r4, #0x4
    add r5, r5, #0x4
    cmp r6, #0x5
    blt ov006_021ffbc4_L52
    ldr r0, [sp]
    ldr r1, =native_fn_021ffc48+1
    bl native_fn_02204970
    add sp, #0xc
    pop {r4, r5, r6, r7, pc}
}
