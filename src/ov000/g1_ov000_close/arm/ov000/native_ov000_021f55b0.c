/* ov000 row 0x021f55b0: 288 bytes.
 *
 * What it does: 72 instructions; 16 call(s) to 0x020624c0, 0x02223ec0, 0x020624c0, +13 more; loops (back edge at +0x08); returns through pop {r4, r5, r6, r7, r8, r9, r10, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x5c -> +0x104
 *   branch +0x9c -> +0xc4
 *   branch +0xa4 -> +0xbc
 *   branch +0xb8 -> +0xc4
 *   branch +0xdc -> +0x104
 *   branch +0xe4 -> +0xfc
 *   branch +0xf8 -> +0x104
 *   back edge +0x10c -> +0x2c
 *   test +0x58 cmp r6, #0
 *   test +0x6c cmp r0, #0
 *   test +0x7c cmp r0, #0
 *   test +0x98 cmp r0, #0
 *   test +0xa0 cmp r10, #0
 *   test +0xd8 cmp r0, #0
 *   test +0xe0 cmp r10, #0
 *   test +0x108 cmp r8, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f55b0; the literal pool and
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

extern void native_fn_020624c0(void);
extern void native_fn_02223ec0(void);
extern void native_fn_02223d40(void);
extern void native_fn_02223d70(void);
extern void native_fn_02223e58(void);
extern void native_fn_02061dcc(void);
extern void native_fn_021f56d0(void);
extern void native_fn_02049ffc(void);
extern void native_fn_02061250(void);
extern void native_fn_02045ed0(void);


asm u32 native_ov000_021f55b0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    mov r0, #19
    bl native_fn_020624c0
    bl native_fn_02223ec0
    mov r0, #19
    bl native_fn_020624c0
    mov r8, #0
    mov r9, r0
    mov r5, r8
    mov r4, r8
    mov r7, #19
ov000_021f55b0_L2c:
    mov r0, r7
    bl native_fn_020624c0
    mov r1, r8, lsl #24
    mov r1, r1, asr #24
    bl native_fn_02223d40
    mov r1, r8, lsl #24
    mov r6, r0
    mov r0, r9
    mov r1, r1, asr #24
    bl native_fn_02223d70
    mov r10, r0
    cmp r6, #0
    beq ov000_021f55b0_L104
    ldrsh r0, [r6, #24]
    mov r1, r8, lsl #24
    mov r1, r1, asr #24
    cmp r0, #0
    mov r0, r9
    moveq r10, r5
    bl native_fn_02223e58
    cmp r0, #0
    add r0, r8, #6
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    movne r10, r4
    bl native_fn_02061dcc
    ldr r0, [r0]
    cmp r0, #0
    beq ov000_021f55b0_Lc4
    cmp r10, #0
    beq ov000_021f55b0_Lbc
    add r0, r8, #6
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_021f56d0
    b ov000_021f55b0_Lc4
ov000_021f55b0_Lbc:
    ldr r0, [r0, #0x4]
    bl native_fn_02049ffc
ov000_021f55b0_Lc4:
    add r0, r8, #9
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02061dcc
    ldr r0, [r0]
    cmp r0, #0
    beq ov000_021f55b0_L104
    cmp r10, #0
    beq ov000_021f55b0_Lfc
    add r0, r8, #9
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_021f56d0
    b ov000_021f55b0_L104
ov000_021f55b0_Lfc:
    ldr r0, [r0, #0x4]
    bl native_fn_02049ffc
ov000_021f55b0_L104:
    add r8, r8, #1
    cmp r8, #3
    blt ov000_021f55b0_L2c
    mov r0, #0
    bl native_fn_02061250
    bl native_fn_02045ed0
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
