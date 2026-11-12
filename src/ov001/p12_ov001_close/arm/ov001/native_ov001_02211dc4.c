/* ov001 row 0x02211dc4: 436 bytes.
 *
 * What it does: 108 instructions; 13 call(s) to 0x022118cc, 0x0205f98c, 0x02211918, +10 more; loops (back edge at +0x08); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 13 calls (108 instructions, 13 calls, 8 branches, 12 back edges, 1 literal slot).
 *
 *   pool +0x1b0 -> native_data_0222e10c (image word 0x0222e10c)
 *   branch +0x3c -> +0x64
 *   branch +0x44 -> +0x88
 *   branch +0x48 -> +0x74
 *   branch +0x50 -> +0x80
 *   branch +0x60 -> +0x88
 *   branch +0x70 -> +0x88
 *   branch +0x7c -> +0x88
 *   branch +0xa4 -> +0xf8
 *   branch +0x104 -> +0x19c
 *   back edge +0x198 -> +0x108
 *   test +0x34 cmp r1, #89
 *   test +0x40 cmp r1, #87
 *   test +0x4c cmp r1, #88
 *   test +0x54 cmp r1, #89
 *   test +0x64 cmp r1, #119
 *   test +0xa0 cmp r1, r6
 *   test +0x100 cmp r4, r0
 *   test +0x120 cmp r4, r0
 *   test +0x194 cmp r4, r0
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02211dc4; the literal pool and
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

extern void native_fn_022118cc(void);
extern void native_fn_0205f98c(void);
extern void native_fn_02211918(void);
extern void native_fn_02048a60(void);
extern void native_fn_02048a94(void);
extern void native_fn_02048a9c(void);
extern u8 native_data_0222e10c[];


asm u32 native_ov001_02211dc4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r10, r0
    bl native_fn_022118cc
    ldr r0, [r10, #0x1c]
    mov r1, #0
    bl native_fn_0205f98c
    mov r1, #6
    str r1, [r0, #0x84]
    mov r0, r10
    bl native_fn_02211918
    ldrsh r2, [r10, #22]
    ldr r1, [r10, #0x30]
    mov r5, r0
    cmp r1, #89
    and r11, r2, #255
    bgt ov001_02211dc4_L64
    cmp r1, #87
    blt ov001_02211dc4_L88
    beq ov001_02211dc4_L74
    cmp r1, #88
    beq ov001_02211dc4_L80
    cmp r1, #89
    moveq r7, #55
    moveq r6, #45
    b ov001_02211dc4_L88
ov001_02211dc4_L64:
    cmp r1, #119
    moveq r7, #131
    moveq r6, #121
    b ov001_02211dc4_L88
ov001_02211dc4_L74:
    mov r7, #75
    mov r6, #65
    b ov001_02211dc4_L88
ov001_02211dc4_L80:
    mov r7, #35
    mov r6, #25
ov001_02211dc4_L88:
    mov r4, #1
    ldr r0, [r10, #0x1c]
    mov r1, r4
    bl native_fn_0205f98c
    mov r8, r0
    ldrb r1, [r8, #0x4]
    cmp r1, r6
    bhs ov001_02211dc4_Lf8
    mov r1, r5
    mov r2, r11
    bl native_fn_02048a60
    ldrb r1, [r10, #0x20]
    mov r0, r8
    sub r1, r1, #1
    and r1, r1, #255
    bl native_fn_02048a94
    ldrb r1, [r10, #0x21]
    mov r0, r8
    bl native_fn_02048a9c
    ldr r0, [r8, #0x7c]
    add r2, r5, #9
    orr r1, r0, #2
    add r0, r4, #1
    str r1, [r8, #0x7c]
    mov r1, #6
    str r1, [r8, #0x84]
    and r5, r2, #255
    and r4, r0, #255
ov001_02211dc4_Lf8:
    ldrb r0, [r10, #0x22]
    str r4, [sp]
    cmp r4, r0
    bhs ov001_02211dc4_L19c
ov001_02211dc4_L108:
    ldr r0, [r10, #0x1c]
    mov r1, r4
    bl native_fn_0205f98c
    mov r9, r0
    ldr r0, [sp]
    ldrb r2, [r9, #0x4]
    cmp r4, r0
    movne r3, r7
    moveq r3, r6
    sub r3, r2, r3
    mov r0, r9
    mov r1, r5
    mov r2, r11
    and r8, r3, #255
    bl native_fn_02048a60
    ldrb r1, [r10, #0x20]
    mov r0, r9
    sub r1, r1, #1
    and r1, r1, #255
    bl native_fn_02048a94
    ldrb r1, [r10, #0x21]
    mov r0, r9
    bl native_fn_02048a9c
    ldr r0, =native_data_0222e10c
    add r1, r4, #1
    ldrb r2, [r0, r8]
    ldr r0, [r9, #0x7c]
    and r4, r1, #255
    orr r0, r0, #2
    str r0, [r9, #0x7c]
    mov r0, #6
    str r0, [r9, #0x84]
    ldrb r0, [r10, #0x22]
    add r2, r5, r2
    and r5, r2, #255
    cmp r4, r0
    blo ov001_02211dc4_L108
ov001_02211dc4_L19c:
    mov r0, #50
    strh r0, [r10, #38]
    mov r0, #1
    strb r0, [r10, #0x24]
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
