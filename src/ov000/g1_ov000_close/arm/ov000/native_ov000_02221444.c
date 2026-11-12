/* ov000 row 0x02221444: 104 bytes.
 *
 * What it does: 24 instructions; 3 call(s) to 0x0222189c, 0x0203ccd0, 0x0203cf9c; loops (back edge at +0x28); returns through pop {r3, r4, r5, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x60 -> constant 0x02246428 (image word 0x02246428)
 *   pool +0x64 -> constant 0x00363144 (image word 0x00363144)
 *   branch +0x18 -> +0x20
 *   branch +0x30 -> +0x58
 *   branch +0x4c -> +0x58
 *   test +0x14 cmp r0, #0
 *   test +0x44 cmp r2, r0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02221444; the literal pool and
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

extern void native_fn_0222189c(void);
extern void native_fn_0203ccd0(void);
extern void native_fn_0203cf9c(void);


asm u32 native_ov000_02221444 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r1, =0x02246428
    mov r5, r0
    ldr r0, [r1]
    mov r4, #0
    cmp r0, #0
    beq ov000_02221444_L20
    bl native_fn_0222189c
ov000_02221444_L20:
    mov r0, r5
    mov r1, #1
    bl native_fn_0203ccd0
    movs r1, r0
    beq ov000_02221444_L58
    ldr r2, =0x02246428
    ldr r0, =0x00363144
    str r1, [r2]
    ldr r2, [r1]
    cmp r2, r0
    moveq r4, #1
    beq ov000_02221444_L58
    mov r0, #1
    bl native_fn_0203cf9c
ov000_02221444_L58:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, pc}
}
