/* ov000 row 0x021f8aac: 96 bytes.
 *
 * What it does: 24 instructions; 6 call(s) to 0x02215698, 0x021f9614, 0x021f94d0, +3 more; loops (back edge at +0x40); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x30 -> +0x48
 *   branch +0x44 -> +0x58
 *   test +0x24 cmp r5, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f8aac; the literal pool and
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

extern void ov000_display_context_02215698(void);
extern void native_fn_021f9614(void);
extern void native_fn_021f94d0(void);
extern void native_fn_0205fb3c(void);
extern void native_fn_021f950c(void);


asm u32 native_ov000_021f8aac (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r6, r0
    mov r5, r1
    bl ov000_display_context_02215698
    add r1, r0, #184
    mov r0, #80
    mla r4, r6, r0, r1
    mov r0, r6
    bl native_fn_021f9614
    cmp r5, #0
    ldrb r1, [r4, #0x4e]
    mov r0, r4
    beq ov000_021f8aac_L48
    bl native_fn_021f94d0
    mov r0, r4
    mov r1, #2
    bl native_fn_0205fb3c
    b ov000_021f8aac_L58
ov000_021f8aac_L48:
    bl native_fn_021f950c
    mov r0, r4
    mov r1, #1
    bl native_fn_0205fb3c
ov000_021f8aac_L58:
    mov r0, #1
    ldmia sp!, {r4, r5, r6, pc}
}
