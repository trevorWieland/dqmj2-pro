/* ov000 row 0x022038cc: 324 bytes.
 *
 * What it does: 80 instructions; 16 call(s) to 0x02061944, 0x0206ea80, 0x022032e8, +13 more; loops (back edge at +0x08); returns through pop {r3, r4, r5, r6, r7, r8, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x140 -> constant 0x02238190 (image word 0x02238190)
 *   branch +0x30 -> +0x40
 *   branch +0x38 -> +0x54
 *   branch +0x3c -> +0x10c
 *   branch +0x5c -> +0xb8
 *   back edge +0xac -> +0x7c
 *   branch +0xe0 -> +0x10c
 *   branch +0x118 -> +0x134
 *   branch +0x120 -> +0x130
 *   test +0x2c cmp r0, #0
 *   test +0x34 cmp r0, #1
 *   test +0x58 cmp r0, #0
 *   test +0xa8 cmp r7, #9
 *   test +0xdc cmp r0, r1
 *   test +0xe8 cmp r5, #1
 *   test +0x114 cmp r0, #42
 *   test +0x11c cmp r0, #10
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022038cc; the literal pool and
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

extern void native_fn_02061944(void);
extern void native_fn_0206ea80(void);
extern void native_fn_022032e8(void);
extern void native_fn_02203a10(void);
extern void native_fn_02062328(void);
extern void native_fn_02062144(void);
extern void native_fn_02203688(void);
extern void native_fn_02061dcc(void);
extern void native_fn_02049f4c(void);
extern void native_fn_02203b7c(void);
extern void native_fn_022036f4(void);
extern void native_fn_0206238c(void);
extern void native_fn_020620b4(void);
extern void native_fn_02062358(void);
extern void native_fn_02214a38(void);


asm u32 native_ov000_022038cc (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, lr}
    sub sp, sp, #4
    bl native_fn_02061944
    mov r4, r0
    bl native_fn_0206ea80
    add r1, r4, #512
    ldrsb r2, [r1, #105]
    mov r5, r0
    mov r6, #0
    strb r2, [sp]
    ldrsb r0, [r1, #106]
    cmp r0, #0
    beq ov000_022038cc_L40
    cmp r0, #1
    beq ov000_022038cc_L54
    b ov000_022038cc_L10c
ov000_022038cc_L40:
    bl native_fn_022032e8
    bl native_fn_02203a10
    mov r0, #1
    strb r0, [r4, #0x26a]
    strb r0, [r5, #0xc]
ov000_022038cc_L54:
    ldrsb r0, [r5, #12]
    cmp r0, #0
    beq ov000_022038cc_Lb8
    bl native_fn_02062328
    add r0, r4, #512
    ldrsb r0, [r0, #111]
    mov r1, #0
    bl native_fn_02062144
    bl native_fn_02203688
    mov r7, #0
ov000_022038cc_L7c:
    add r0, r7, #6
    mov r0, r0, lsl #24
    mov r8, r0, asr #24
    mov r0, r8
    bl native_fn_02061dcc
    bl native_fn_02049f4c
    mov r0, r8
    bl native_fn_02203b7c
    add r0, r7, #1
    mov r0, r0, lsl #24
    mov r7, r0, asr #24
    cmp r7, #9
    blt ov000_022038cc_L7c
    mov r0, #0
    strb r0, [r5, #0xc]
ov000_022038cc_Lb8:
    bl native_fn_022036f4
    add r0, sp, #0
    mov r1, #12
    mov r2, #13
    bl native_fn_0206238c
    add r1, r4, #512
    mov r5, r0
    ldrsb r0, [sp]
    ldrsb r1, [r1, #105]
    cmp r0, r1
    beq ov000_022038cc_L10c
    bl native_fn_020620b4
    cmp r5, #1
    movne r0, #0
    moveq r0, #1
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02062358
    ldr r0, =0x02238190
    mov r6, #1
    strb r6, [r0, #0x4]
ov000_022038cc_L10c:
    add r0, r4, #512
    ldrsb r0, [r0, #108]
    cmp r0, #42
    beq ov000_022038cc_L134
    cmp r0, #10
    bne ov000_022038cc_L130
    mov r0, #0
    mov r1, r0
    bl native_fn_02214a38
ov000_022038cc_L130:
    mov r6, #1
ov000_022038cc_L134:
    mov r0, r6
    add sp, sp, #4
    ldmia sp!, {r3, r4, r5, r6, r7, r8, pc}
}
