/* ov000 row 0x02222a40: 168 bytes.
 *
 * What it does: 40 instructions; 10 call(s) to 0x020406a8, 0x020642dc, 0x02222a88, +7 more; loops (back edge at +0x0c); returns through pop {r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xa0 -> constant 0x02246584 (image word 0x02246584)
 *   pool +0xa4 -> constant 0x02246574 (image word 0x02246574)
 *   branch +0x18 -> +0x38
 *   branch +0x20 -> +0x48
 *   branch +0x24 -> +0x4c
 *   branch +0x30 -> +0x40
 *   branch +0x34 -> +0x48
 *   branch +0x3c -> +0x48
 *   branch +0x44 -> +0x4c
 *   test +0x14 cmp r0, #4
 *   test +0x1c cmp r0, #2
 *   test +0x28 cmp r0, #3
 *   test +0x2c cmpne r0, #4
 *   test +0x38 cmp r0, #51
 *   test +0x50 cmp r0, #47
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02222a40; the literal pool and
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

extern void native_fn_020406a8(void);
extern void native_fn_020642dc(void);
extern void native_fn_020612ec(void);
extern void native_fn_0206dcd0(void);
extern void native_fn_02061950(void);
extern void native_fn_020bb334(void);
extern void native_fn_0204baec(void);
extern void native_fn_0204b9d0(void);


asm u32 native_ov000_02222a40 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r0, #1
    mov r4, #16
    bl native_fn_020406a8
    bl native_fn_020642dc
    cmp r0, #4
    bgt ov000_02222a40_L38
    cmp r0, #2
    blt ov000_02222a40_L48
    beq ov000_02222a40_L4c
    cmp r0, #3
    cmpne r0, #4
    beq ov000_02222a40_L40
    b ov000_02222a40_L48
ov000_02222a40_L38:
    cmp r0, #51
    bne ov000_02222a40_L48
ov000_02222a40_L40:
    mov r4, #27
    b ov000_02222a40_L4c
ov000_02222a40_L48:
    mov r4, #0
ov000_02222a40_L4c:
    bl native_fn_020642dc
    cmp r0, #47
    moveq r4, #16
    mov r0, r4
    mov r1, #1
    mov r2, #32768
    mov r3, #0
    bl native_fn_020612ec
    mov r0, #0
    bl native_fn_0206dcd0
    mov r0, #16
    bl native_fn_02061950
    bl native_fn_020bb334
    bl native_fn_0204baec
    ldr r1, =0x02246584
    bl native_fn_0204b9d0
    ldr r0, =0x02246574
    mov r1, #1
    strb r1, [r0]
    mov r0, #0
    ldmia sp!, {r4, pc}
}
