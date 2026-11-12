/* ov000 row 0x02220714: 100 bytes.
 *
 * What it does: 24 instructions; 3 call(s) to 0x0222076c, 0x0222136c, 0x02062b0c; loops (back edge at +0x44); returns through pop {r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x60 -> constant 0x022463b0 (image word 0x022463b0)
 *   branch +0x1c -> +0x58
 *   branch +0x30 -> +0x58
 *   branch +0x38 -> +0x50
 *   branch +0x4c -> +0x58
 *   test +0x10 cmp r1, #10
 *   test +0x18 cmphs r1, #10
 *   test +0x24 cmp r1, #2
 *   test +0x2c cmpeq r1, #2
 *   test +0x34 cmp r0, #0
 *   test +0x48 cmp r4, r0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02220714; the literal pool and
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

extern void native_fn_0222136c(void);
extern void native_fn_02062b0c(void);


asm u32 native_ov000_02220714 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r1, =0x022463b0
    ldr r2, [r1, #0x1c]
    ldrb r1, [r2, #0x30]
    cmp r1, #10
    ldrhsb r1, [r2, #0xb4]
    cmphs r1, #10
    blo ov000_02220714_L58
    ldrb r1, [r2, #0x1b]
    cmp r1, #2
    ldreqb r1, [r2, #0x9f]
    cmpeq r1, #2
    beq ov000_02220714_L58
    cmp r0, #0
    beq ov000_02220714_L50
    bl native_fn_0222136c
    mov r4, r0
    bl native_fn_02062b0c
    cmp r4, r0
    bgt ov000_02220714_L58
ov000_02220714_L50:
    mov r0, #1
    ldmia sp!, {r4, pc}
ov000_02220714_L58:
    mov r0, #0
    ldmia sp!, {r4, pc}
}
