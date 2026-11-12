/* ov000 row 0x021e0d78: 140 bytes.
 *
 * What it does: 33 instructions; 6 call(s) to 0x021e0bdc, 0x021e0bec, 0x021e31f0, +3 more; loops (back edge at +0x14); returns through pop {r4, r5, r6, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x84 -> constant 0x022322d4 (image word 0x022322d4)
 *   pool +0x88 -> constant 0x022322d0 (image word 0x022322d0)
 *   branch +0x1c -> +0x4c
 *   branch +0x38 -> +0x54
 *   branch +0x48 -> +0x54
 *   test +0x18 cmp r0, #0
 *   test +0x34 cmp r0, #0
 *   test +0x64 cmp r0, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e0d78; the literal pool and
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

extern void native_fn_021e0bdc(void);
extern void native_fn_021e0bec(void);
extern void native_fn_021e31f0(void);
extern void native_fn_021e3370(void);
extern void native_fn_02042464(void);
extern void native_fn_021e0cf8(void);


asm u32 native_ov000_021e0d78 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    ldr r4, =0x022322d4
    mov r6, r0
    mov r5, r1
    strb r2, [r4, #0x15f]
    bl native_fn_021e0bdc
    cmp r0, #0
    beq ov000_021e0d78_L4c
    mov r0, r6
    bl native_fn_021e0bec
    ldr r1, =0x022322d0
    mov r6, r0
    ldrsb r0, [r1]
    cmp r0, #0
    bge ov000_021e0d78_L54
    mov r0, #9
    mov r1, #1
    bl native_fn_021e31f0
    b ov000_021e0d78_L54
ov000_021e0d78_L4c:
    mov r0, #0
    bl native_fn_021e3370
ov000_021e0d78_L54:
    mov r0, r4
    mov r1, r6
    mov r2, r5
    bl native_fn_02042464
    cmp r0, #0
    moveq r0, #0
    ldmeqia sp!, {r4, r5, r6, pc}
    mov r0, r6
    bl native_fn_021e0cf8
    str r0, [r4, #0x264]
    mov r0, #1
    ldmia sp!, {r4, r5, r6, pc}
}
