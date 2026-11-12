/* ov000 row 0x022221e4: 556 bytes.
 *
 * What it does: 137 instructions; 25 call(s) to 0x02215a14, 0x022159b8, 0x02068bd4, +22 more; loops (back edge at +0x18); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x224 -> native_data_0222fbe8 (image word 0x0222fbe8)
 *   pool +0x228 -> native_data_0222fc00 (image word 0x0222fc00)
 *   branch +0x54 -> +0xa4
 *   back edge +0xac -> +0x48
 *   branch +0xd8 -> +0x128
 *   back edge +0x130 -> +0xcc
 *   branch +0x1d0 -> +0x20c
 *   back edge +0x214 -> +0x1b4
 *   test +0x6c cmp r0, #0
 *   test +0xa8 cmp r8, #3
 *   test +0xf0 cmp r0, #0
 *   test +0x12c cmp r10, #3
 *   test +0x1cc cmp r0, #0
 *   test +0x1e0 cmp r8, #0
 *   test +0x210 cmp r9, #6
 *   2 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022221e4; the literal pool and
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

extern void native_fn_02215a14(void);
extern u8 native_data_0222fbe8[];
extern void native_fn_022159b8(void);
extern void native_fn_02068bd4(void);
extern void native_fn_02062a50(void);
extern void native_fn_02062a10(void);
extern void native_fn_020692b0(void);
extern void native_fn_02044cdc(void);
extern void native_fn_02062a88(void);
extern void native_fn_02068c14(void);
extern u8 native_data_0222fc00[];
extern void native_fn_020451c4(void);
extern void native_fn_020482b4(void);
extern void native_fn_0204532c(void);
extern void native_fn_0206c0a0(void);
extern void native_fn_0221744c(void);
extern void native_fn_0206c718(void);
extern void native_fn_02048308(void);


asm u32 native_ov000_022221e4 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #20
    mov r2, #0
    str r0, [sp, #0xc]
    mov r4, r1
    str r2, [sp, #0x10]
    bl native_fn_02215a14
    ldr r0, =native_data_0222fbe8
    mov r1, #4
    bl native_fn_022159b8
    mov r0, r4
    bl native_fn_02068bd4
    mov r9, #0
    mov r8, r9
    mov r5, #18
    mov r7, #12
    mov r6, #15
    mov r4, r9
ov000_022221e4_L48:
    mov r0, r8
    bl native_fn_02062a50
    movs r10, r0
    beq ov000_022221e4_La4
    ldr r0, [r10, #0x14]
    bl native_fn_02062a10
    ldrb r0, [r0, #0x33]
    mov r2, r4
    and r3, r9, #255
    cmp r0, #0
    moveq r0, r7
    moveq r1, r6
    movne r0, r5
    movne r1, r5
    str r4, [sp]
    stmib sp, {r0, r1}
    ldr r0, [r10, #0x14]
    mov r1, r4
    bl native_fn_020692b0
    ldrsh r0, [r10, #24]
    bl native_fn_02044cdc
    add r0, r0, #1
    add r9, r9, r0
ov000_022221e4_La4:
    add r8, r8, #1
    cmp r8, #3
    blt ov000_022221e4_L48
    mov r9, #0
    mov r10, r9
    mov r11, #18
    mov r7, #12
    mov r6, #15
    mov r5, r9
    mov r4, #1
ov000_022221e4_Lcc:
    mov r0, r10
    bl native_fn_02062a88
    movs r8, r0
    beq ov000_022221e4_L128
    ldr r0, [r8, #0x14]
    bl native_fn_02062a10
    ldrb r0, [r0, #0x33]
    mov r2, r5
    and r3, r9, #255
    cmp r0, #0
    moveq r0, r7
    moveq r1, r6
    movne r0, r11
    movne r1, r11
    str r5, [sp]
    stmib sp, {r0, r1}
    ldr r0, [r8, #0x14]
    mov r1, r4
    bl native_fn_020692b0
    ldrsh r0, [r8, #24]
    bl native_fn_02044cdc
    add r0, r0, #1
    add r9, r9, r0
ov000_022221e4_L128:
    add r10, r10, #1
    cmp r10, #3
    blt ov000_022221e4_Lcc
    mov r2, #0
    str r2, [sp]
    mov r1, #12
    str r1, [sp, #0x4]
    mov r4, #15
    ldr r0, [sp, #0xc]
    mov r3, r2
    mov r1, #2
    str r4, [sp, #0x8]
    bl native_fn_020692b0
    mov r0, #2
    mov r1, #36
    mov r2, #32
    mov r3, #0
    bl native_fn_02068c14
    ldr r0, =native_data_0222fc00
    add r3, sp, #16
    mov r1, #17
    mov r2, #2
    bl native_fn_020451c4
    mov r4, r0
    mov r1, #352
    mov r2, #32
    bl native_fn_020482b4
    mov r1, r4
    mov r0, #2
    bl native_fn_0204532c
    mov r9, #0
    mov r5, #12
    mov r6, #18
    mov r4, r9
    mov r11, #1
ov000_022221e4_L1b4:
    mov r0, r9, lsl #24
    mov r0, r0, asr #24
    bl native_fn_0206c0a0
    mov r7, r0
    ldr r0, [r7]
    bl native_fn_02062a10
    cmp r0, #0
    beq ov000_022221e4_L20c
    ldr r0, [r0, #0x14]
    bl native_fn_02062a10
    ldrb r8, [r0, #0x33]
    cmp r8, #0
    movne r10, r6
    moveq r10, r5
    bl native_fn_0221744c
    str r4, [sp]
    and r1, r10, #255
    str r1, [sp, #0x4]
    ldrsb r2, [r7, #12]
    mov r1, r11
    mov r3, r8
    bl native_fn_0206c718
ov000_022221e4_L20c:
    add r9, r9, #1
    cmp r9, #6
    blt ov000_022221e4_L1b4
    bl native_fn_02048308
    add sp, sp, #20
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
