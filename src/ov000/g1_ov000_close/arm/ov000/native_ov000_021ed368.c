/* ov000 row 0x021ed368: 156 bytes.
 *
 * What it does: 38 instructions; 5 call(s) to 0x020c48bc, 0x020c48d0, 0x020c48d0, +2 more; loops (back edge at +0x2c); returns through pop {r3, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x98 -> constant 0x02236bc4 (image word 0x02236bc4)
 *   branch +0x40 -> +0x54
 *   branch +0x48 -> +0x68
 *   branch +0x50 -> +0x7c
 *   branch +0x64 -> +0x8c
 *   branch +0x78 -> +0x8c
 *   test +0x20 cmp r0, #3
 *   test +0x3c cmp r0, #0
 *   test +0x44 cmp r0, #1
 *   test +0x4c cmp r0, #2
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021ed368; the literal pool and
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

extern void native_fn_020c48bc(void);
extern void native_fn_020c48d0(void);
extern void native_fn_020c48e8(void);


asm u32 native_ov000_021ed368 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, =0x02236bc4
    ldr r2, [r0, #0x4]
    ldrb r1, [r2, #0x50a]
    add r1, r1, #1
    strb r1, [r2, #0x50a]
    ldr r1, [r0, #0x4]
    ldrb r0, [r1, #0x50a]
    cmp r0, #3
    movhs r0, #0
    strhsb r0, [r1, #0x50a]
    bl native_fn_020c48bc
    ldr r0, =0x02236bc4
    ldr r0, [r0, #0x4]
    ldrb r0, [r0, #0x50a]
    cmp r0, #0
    beq ov000_021ed368_L54
    cmp r0, #1
    beq ov000_021ed368_L68
    cmp r0, #2
    b ov000_021ed368_L7c
ov000_021ed368_L54:
    mov r0, #5
    mov r1, #8
    mov r2, #34
    bl native_fn_020c48d0
    b ov000_021ed368_L8c
ov000_021ed368_L68:
    mov r0, #5
    mov r1, #8
    mov r2, #35
    bl native_fn_020c48d0
    b ov000_021ed368_L8c
ov000_021ed368_L7c:
    mov r0, #5
    mov r1, #8
    mov r2, #33
    bl native_fn_020c48d0
ov000_021ed368_L8c:
    mov r0, #87
    bl native_fn_020c48e8
    ldmia sp!, {r3, pc}
}
