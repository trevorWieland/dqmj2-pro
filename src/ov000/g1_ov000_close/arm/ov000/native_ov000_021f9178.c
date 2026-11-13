/* ov000 row 0x021f9178: 260 bytes.
 *
 * What it does: 65 instructions; 8 call(s) to 0x02215698, 0x02062aa0, 0x021f9258, +5 more; loops (back edge at +0x70); returns through pop {r4, r5, r6, r7, r8, r9, r10, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x44 -> +0x54
 *   branch +0x5c -> +0x68
 *   branch +0x6c -> +0x7c
 *   branch +0x80 -> +0xf0
 *   branch +0xa4 -> +0xe0
 *   back edge +0xdc -> +0xa8
 *   branch +0xec -> +0xfc
 *   test +0x2c cmp r4, #3
 *   test +0x48 cmp r4, #0
 *   test +0x54 cmp r6, #2
 *   test +0x60 cmp r6, #0
 *   test +0x68 cmp r7, #0
 *   test +0x74 cmp r0, #0
 *   test +0x7c cmp r7, #0
 *   test +0x9c cmp r0, #0
 *   test +0xb0 cmp r8, r0
 *   test +0xd8 cmp r10, r0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f9178; the literal pool and
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

extern void ov000_display_context_02215698(void);
extern void native_fn_02062aa0(void);
extern void native_fn_0206d250(void);
extern void native_fn_021f962c(void);
extern void native_fn_021f9148(void);
extern void native_fn_021f9118(void);


asm u32 native_ov000_021f9178 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    mov r7, r0
    mov r5, r2
    mov r6, r1
    mov r4, r3
    bl ov000_display_context_02215698
    add r1, r7, r5
    mov r1, r1, lsl #24
    add r2, r6, r4
    mov r4, r1, asr #24
    mov r1, r2, lsl #24
    cmp r4, #3
    mov r7, #1
    movgt r4, #0
    mov r5, r0
    mov r6, r1, asr #24
    movgt r7, r4
    bgt ov000_021f9178_L54
    cmp r4, #0
    movlt r4, #3
    movlt r7, #0
ov000_021f9178_L54:
    cmp r6, #2
    movgt r6, #0
    bgt ov000_021f9178_L68
    cmp r6, #0
    movlt r6, #2
ov000_021f9178_L68:
    cmp r7, #0
    bne ov000_021f9178_L7c
    bl native_fn_02062aa0
    cmp r0, #0
    moveq r7, #1
ov000_021f9178_L7c:
    cmp r7, #0
    bne ov000_021f9178_Lf0
    mov r0, #40
    mul r1, r6, r0
    add r4, r5, #1024
    ldrsb r0, [r4, #149]
    mov r9, #0
    mov r10, r9
    cmp r0, #0
    add r8, r1, #48
    ble ov000_021f9178_Le0
ov000_021f9178_La8:
    add r0, r5, r10, lsl #3
    ldrb r0, [r0, #0xa5]
    cmp r8, r0
    moveq r0, r9, lsl #24
    moveq r6, r0, asr #24
    add r0, r5, r10, lsl #3
    ldrsb r0, [r0, #166]
    bl native_fn_0206d250
    add r1, r0, #1
    ldrsb r0, [r4, #149]
    add r10, r10, #1
    add r9, r9, r1
    cmp r10, r0
    blt ov000_021f9178_La8
ov000_021f9178_Le0:
    mov r0, r6
    bl native_fn_021f962c
    bl native_fn_021f9148
    b ov000_021f9178_Lfc
ov000_021f9178_Lf0:
    mov r0, r4
    mov r1, r6
    bl native_fn_021f9118
ov000_021f9178_Lfc:
    mov r0, r7
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
