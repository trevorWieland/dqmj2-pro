/* ov000 row 0x02224804: 112 bytes.
 *
 * What it does: 28 instructions; 5 call(s) to 0x020633b0, 0x02062a10, 0x02062a10, +2 more; loops (back edge at +0x04); returns through pop {r3, r4, r5, r6, r7, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x24 -> +0x30
 *   branch +0x2c -> +0x34
 *   back edge +0x4c -> +0x18
 *   branch +0x54 -> +0x68
 *   test +0x1c cmp r5, #3
 *   test +0x34 cmp r0, #0
 *   test +0x48 cmp r5, #6
 *   test +0x50 cmp r6, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02224804; the literal pool and
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

extern void native_fn_020633b0(void);
extern void native_fn_02062a10(void);
extern void native_fn_02026144(void);


asm u32 native_ov000_02224804 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    bl native_fn_020633b0
    mov r6, #0
    mov r4, r0
    mov r7, r6
    mov r5, r6
ov000_02224804_L18:
    add r0, r4, r5, lsl #2
    cmp r5, #3
    ldr r0, [r0, #0x1c]
    bge ov000_02224804_L30
    bl native_fn_02062a10
    b ov000_02224804_L34
ov000_02224804_L30:
    bl native_fn_02062a10
ov000_02224804_L34:
    cmp r0, #0
    ldrneb r0, [r0, #0x30]
    add r5, r5, #1
    addne r6, r6, #1
    addne r7, r7, r0
    cmp r5, #6
    blt ov000_02224804_L18
    cmp r6, #0
    beq ov000_02224804_L68
    mov r0, r7
    mov r1, r6
    bl native_fn_02026144
    mov r7, r0
ov000_02224804_L68:
    and r0, r7, #255
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
