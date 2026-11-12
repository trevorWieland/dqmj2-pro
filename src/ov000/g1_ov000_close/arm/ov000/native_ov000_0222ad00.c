/* ov000 row 0x0222ad00: 148 bytes.
 *
 * What it does: 35 instructions; 5 call(s) to 0x0202a634, 0x02063b28, 0x0205e7a8, +2 more; loops (back edge at +0x0c); returns through pop {r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x8c -> constant 0x022475ec (image word 0x022475ec)
 *   pool +0x90 -> constant 0x022475dc (image word 0x022475dc)
 *   branch +0x1c -> +0x84
 *   branch +0x28 -> +0x84
 *   branch +0x40 -> +0x60
 *   branch +0x5c -> +0x78
 *   test +0x18 cmp r2, #0
 *   test +0x24 tst r0, #1
 *   test +0x3c cmp r0, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0222ad00; the literal pool and
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

extern void native_fn_0202a634(void);
extern void native_fn_02063b28(void);
extern void native_fn_0205e7a8(void);


asm u32 native_ov000_0222ad00 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r0, =0x022475ec
    ldrsb r4, [r0, #32]
    bl native_fn_0202a634
    ldr r1, =0x022475ec
    ldrsb r2, [r1, #32]
    cmp r2, #0
    bne ov000_0222ad00_L84
    ldrh r0, [r0, #2]
    tst r0, #1
    beq ov000_0222ad00_L84
    ldr r1, [r1, #0x10]
    ldr r0, =0x022475dc
    mov r1, r1, lsl #1
    ldrh r0, [r0, r1]
    cmp r0, #0
    bne ov000_0222ad00_L60
    mov r0, #47
    mov r1, #0
    bl native_fn_02063b28
    mvn r0, #0
    mov r1, #83
    bl native_fn_0205e7a8
    b ov000_0222ad00_L78
ov000_0222ad00_L60:
    and r1, r0, #255
    mov r0, #47
    bl native_fn_02063b28
    mvn r0, #0
    mov r1, #82
    bl native_fn_0205e7a8
ov000_0222ad00_L78:
    ldr r0, =0x022475ec
    mov r1, #6
    strb r1, [r0, #0x100]
ov000_0222ad00_L84:
    mov r0, r4
    ldmia sp!, {r4, pc}
}
