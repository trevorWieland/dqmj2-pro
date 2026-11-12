/* ov000 row 0x02227a54: 408 bytes.
 *
 * What it does: 98 instructions; 14 call(s) to 0x02227ccc, 0x02227980, 0x022278f4, +11 more; loops (back edge at +0x1c); returns through pop {r4, r5, r6, r7, r8, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x188 -> constant 0x02246c84 (image word 0x02246c84)
 *   pool +0x18c -> constant 0x02246aa8 (image word 0x02246aa8)
 *   pool +0x190 -> constant 0x022468b8 (image word 0x022468b8)
 *   pool +0x194 -> constant 0x022468ba (image word 0x022468ba)
 *   branch +0x18 -> +0x24
 *   branch +0x20 -> +0x28
 *   branch +0x38 -> +0x50
 *   branch +0x40 -> +0xc8
 *   branch +0x48 -> +0xfc
 *   branch +0x4c -> +0x180
 *   branch +0x70 -> +0xb8
 *   branch +0x7c -> +0x9c
 *   branch +0x88 -> +0x180
 *   branch +0x98 -> +0x180
 *   branch +0xa4 -> +0x180
 *   branch +0xb4 -> +0x180
 *   branch +0xc4 -> +0x180
 *   branch +0xe8 -> +0x180
 *   branch +0xf8 -> +0x180
 *   branch +0x110 -> +0x180
 *   branch +0x134 -> +0x14c
 *   branch +0x148 -> +0x15c
 *   back edge +0x170 -> +0x12c
 *   test +0x14 cmp r0, #0
 *   test +0x34 cmp r1, #0
 *   test +0x3c cmp r1, #1
 *   test +0x44 cmp r1, #2
 *   test +0x6c cmp r0, #0
 *   test +0x78 cmp r0, #0
 *   test +0x84 cmp r0, #0
 *   test +0xa0 cmp r0, #0
 *   test +0xd8 cmp r2, r1
 *   test +0x10c cmp r7, #0
 *   test +0x130 cmp r0, #0
 *   test +0x168 cmp r8, #3
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02227a54; the literal pool and
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

extern void native_fn_02227ccc(void);
extern void native_fn_02227980(void);
extern void native_fn_022278f4(void);
extern void native_fn_01ffa824(void);
extern void native_fn_01ffa5fc(void);
extern void native_fn_0222534c(void);
extern void native_fn_022252ac(void);
extern void native_fn_01ffa5ac(void);
extern void native_fn_02223ce0(void);
extern void native_fn_021f51e8(void);
extern void native_fn_02225eb8(void);


asm u32 native_ov000_02227a54 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    ldr r4, =0x02246c84
    ldr r6, =0x02246aa8
    mov r5, #0
    bl native_fn_02227ccc
    cmp r0, #0
    beq ov000_02227a54_L24
    bl native_fn_02227980
    b ov000_02227a54_L28
ov000_02227a54_L24:
    bl native_fn_022278f4
ov000_02227a54_L28:
    mov r7, r0
    ldr r0, =0x022468b8
    ldrsb r1, [r0, #2]
    cmp r1, #0
    beq ov000_02227a54_L50
    cmp r1, #1
    beq ov000_02227a54_Lc8
    cmp r1, #2
    beq ov000_02227a54_Lfc
    b ov000_02227a54_L180
ov000_02227a54_L50:
    bl native_fn_01ffa824
    ldrb r1, [r4, #0x18e]
    and r0, r0, #255
    add r1, r1, #48
    mov r1, r1, lsl #16
    mov r1, r1, lsr #16
    bl native_fn_01ffa5fc
    cmp r0, #0
    bne ov000_02227a54_Lb8
    bl native_fn_02227ccc
    cmp r0, #0
    beq ov000_02227a54_L9c
    bl native_fn_0222534c
    cmp r0, #0
    bne ov000_02227a54_L180
    ldr r0, =0x022468b8
    mov r1, #1
    strb r1, [r0, #0x2]
    b ov000_02227a54_L180
ov000_02227a54_L9c:
    bl native_fn_022252ac
    cmp r0, #0
    bne ov000_02227a54_L180
    ldr r0, =0x022468b8
    mov r1, #1
    strb r1, [r0, #0x2]
    b ov000_02227a54_L180
ov000_02227a54_Lb8:
    ldrb r0, [r4, #0x18e]
    add r0, r0, #1
    strb r0, [r4, #0x18e]
    b ov000_02227a54_L180
ov000_02227a54_Lc8:
    ldrb r2, [r4, #0x190]
    ldrb r1, [r4, #0x18d]
    add r3, r2, #1
    and r2, r3, #255
    cmp r2, r1
    movhs r1, #2
    strb r3, [r4, #0x190]
    strhsb r1, [r0, #0x2]
    bhs ov000_02227a54_L180
    mov r1, #0
    strb r1, [r0, #0x2]
    strb r1, [r4, #0x18e]
    b ov000_02227a54_L180
ov000_02227a54_Lfc:
    ldr r0, =0x022468ba
    mov r1, #1
    mov r2, #63
    bl native_fn_01ffa5ac
    cmp r7, #0
    beq ov000_02227a54_L180
    ldr r0, =0x022468b8
    mov r8, #0
    mov r5, #1
    strb r8, [r0, #0x2]
    mov r4, r8
    mov r7, r5
ov000_02227a54_L12c:
    ldrsh r0, [r6, #24]
    cmp r0, #0
    beq ov000_02227a54_L14c
    mov r0, r7
    mov r1, r8
    mov r2, r6
    bl native_fn_02223ce0
    b ov000_02227a54_L15c
ov000_02227a54_L14c:
    mov r0, r5
    mov r1, r8
    mov r2, r4
    bl native_fn_02223ce0
ov000_02227a54_L15c:
    add r0, r8, #1
    mov r0, r0, lsl #24
    mov r8, r0, asr #24
    cmp r8, #3
    add r6, r6, #132
    blt ov000_02227a54_L12c
    bl native_fn_021f51e8
    bl native_fn_02225eb8
    mov r5, #1
ov000_02227a54_L180:
    mov r0, r5
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
