/* ov000 row 0x021f933c: 328 bytes.
 *
 * What it does: 82 instructions; 14 call(s) to 0x02215698, 0x0202a634, 0x021e7b9c, +11 more; loops (back edge at +0x0c); returns through pop {r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x24 -> +0x40
 *   branch +0x3c -> +0x5c
 *   branch +0x44 -> +0x5c
 *   branch +0x60 -> +0x7c
 *   branch +0x78 -> +0x98
 *   branch +0x80 -> +0x98
 *   branch +0xa0 -> +0x140
 *   branch +0xb0 -> +0xf8
 *   branch +0xcc -> +0x13c
 *   branch +0xf4 -> +0x13c
 *   branch +0xfc -> +0x13c
 *   branch +0x118 -> +0x13c
 *   test +0x20 tst r8, #16
 *   test +0x40 tst r8, #32
 *   test +0x5c tst r8, #128
 *   test +0x7c tst r8, #64
 *   test +0x98 cmp r6, #0
 *   test +0x9c cmpeq r7, #0
 *   test +0xac cmp r0, #1
 *   test +0xc8 cmp r0, #0
 *   test +0xf8 cmp r0, #0
 *   test +0x114 cmp r0, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f933c; the literal pool and
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

extern void native_fn_02215698(void);
extern void native_fn_0202a634(void);
extern void native_fn_021e7b9c(void);
extern void native_fn_021f9178(void);
extern void native_fn_020620b4(void);
extern void native_fn_02062120(void);
extern void native_fn_021f927c(void);
extern void native_fn_0206dcd0(void);


asm u32 native_ov000_021f933c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    bl native_fn_02215698
    mov r4, r0
    bl native_fn_0202a634
    mov r5, #0
    ldrh r8, [r0, #6]
    mov r6, r5
    mov r7, r5
    tst r8, #16
    beq ov000_021f933c_L40
    add r0, r5, #1
    mov r1, r0, lsl #24
    mov r0, #85
    mov r6, r1, asr #24
    bl native_fn_021e7b9c
    b ov000_021f933c_L5c
ov000_021f933c_L40:
    tst r8, #32
    beq ov000_021f933c_L5c
    sub r0, r5, #1
    mov r1, r0, lsl #24
    mov r0, #85
    mov r6, r1, asr #24
    bl native_fn_021e7b9c
ov000_021f933c_L5c:
    tst r8, #128
    beq ov000_021f933c_L7c
    add r0, r7, #1
    mov r1, r0, lsl #24
    mov r0, #85
    mov r7, r1, asr #24
    bl native_fn_021e7b9c
    b ov000_021f933c_L98
ov000_021f933c_L7c:
    tst r8, #64
    beq ov000_021f933c_L98
    sub r0, r7, #1
    mov r1, r0, lsl #24
    mov r0, #85
    mov r7, r1, asr #24
    bl native_fn_021e7b9c
ov000_021f933c_L98:
    cmp r6, #0
    cmpeq r7, #0
    beq ov000_021f933c_L140
    add r1, r4, #1024
    ldrsb r0, [r1, #154]
    cmp r0, #1
    bne ov000_021f933c_Lf8
    ldrsb r0, [r1, #144]
    ldrsb r1, [r1, #145]
    mov r2, r6
    mov r3, r7
    bl native_fn_021f9178
    cmp r0, #0
    bne ov000_021f933c_L13c
    mov r1, #0
    mov r0, #1
    strb r1, [r4, #0x49a]
    bl native_fn_020620b4
    add r0, r4, #1024
    ldrsb r0, [r0, #145]
    bl native_fn_02062120
    mov r0, #86
    bl native_fn_021e7b9c
    b ov000_021f933c_L13c
ov000_021f933c_Lf8:
    cmp r0, #0
    bne ov000_021f933c_L13c
    ldrsb r0, [r1, #144]
    ldrsb r1, [r1, #145]
    mov r2, r6
    mov r3, r7
    bl native_fn_021f927c
    cmp r0, #0
    beq ov000_021f933c_L13c
    mov r1, #1
    mov r0, #0
    strb r1, [r4, #0x49a]
    bl native_fn_020620b4
    mov r0, #0
    bl native_fn_0206dcd0
    mov r0, #86
    bl native_fn_021e7b9c
ov000_021f933c_L13c:
    mov r5, #1
ov000_021f933c_L140:
    mov r0, r5
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
