/* ov000 row 0x02218140: 212 bytes.
 *
 * What it does: 51 instructions; 6 call(s) to 0x02218218, 0x020407ec, 0x02041538, +3 more; loops (back edge at +0x48); returns through pop {r4, r5, r6, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xcc -> constant 0x02245e54 (image word 0x02245e54)
 *   pool +0xd0 -> constant 0x02245eac (image word 0x02245eac)
 *   branch +0x1c -> +0x34
 *   branch +0x24 -> +0x7c
 *   branch +0x2c -> +0xa4
 *   branch +0x30 -> +0xb4
 *   branch +0x44 -> +0x70
 *   branch +0x50 -> +0x64
 *   branch +0x78 -> +0xb4
 *   branch +0x84 -> +0xb4
 *   branch +0xa0 -> +0xb4
 *   branch +0xb8 -> +0xc4
 *   back edge +0xbc -> +0x00
 *   test +0x14 cmp r1, #0
 *   test +0x20 cmp r1, #1
 *   test +0x28 cmp r1, #2
 *   test +0x40 cmp r0, #0
 *   test +0x4c cmp r0, #0
 *   test +0x80 cmp r0, r5
 *   test +0xb4 cmp r6, #0
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02218140; the literal pool and
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

extern void native_fn_02218218(void);
extern void native_fn_020407ec(void);
extern void native_fn_02041538(void);
extern void native_fn_02218d30(void);
extern void native_fn_022193dc(void);


asm u32 native_ov000_02218140 (register u32 a0)
{
ov000_02218140_L0:
    stmdb sp!, {r4, r5, r6, lr}
    ldr r0, =0x02245e54
    ldr r4, =0x02245eac
    ldr r1, [r0, #0x5c]
    ldr r5, [r0, #0x58]
    cmp r1, #0
    mov r6, #0
    beq ov000_02218140_L34
    cmp r1, #1
    beq ov000_02218140_L7c
    cmp r1, #2
    beq ov000_02218140_La4
    b ov000_02218140_Lb4
ov000_02218140_L34:
    bl native_fn_02218218
    ldr r0, =0x02245e54
    ldr r0, [r0, #0xc]
    cmp r0, #0
    beq ov000_02218140_L70
    bl native_fn_020407ec
    cmp r0, #0
    bne ov000_02218140_L64
    mov r0, r6
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
ov000_02218140_L64:
    ldr r0, =0x02245e54
    mov r1, #0
    str r1, [r0, #0xc]
ov000_02218140_L70:
    mov r6, #1
    str r6, [r4, #0x4]
    b ov000_02218140_Lb4
ov000_02218140_L7c:
    bl native_fn_02218d30
    cmp r0, r5
    beq ov000_02218140_Lb4
    ldr r2, [r4]
    mov r1, #2
    str r2, [r4, #0xc]
    str r1, [r4, #0x4]
    str r0, [r4, #0x8]
    mov r6, #1
    b ov000_02218140_Lb4
ov000_02218140_La4:
    bl native_fn_022193dc
    mov r0, r6
    ldr r5, [r4, #0x8]
    str r0, [r4, #0x4]
ov000_02218140_Lb4:
    cmp r6, #0
    beq ov000_02218140_Lc4
    bl ov000_02218140_L0
    mov r5, r0
ov000_02218140_Lc4:
    mov r0, r5
    ldmia sp!, {r4, r5, r6, pc}
}
