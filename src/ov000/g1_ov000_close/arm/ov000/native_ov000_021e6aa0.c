/* ov000 row 0x021e6aa0: 124 bytes.
 *
 * What it does: 31 instructions; 7 call(s) to 0x021e63a4, 0x021e63c8, 0x0202859c, +4 more; loops (back edge at +0x0c); returns through pop {r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x40 -> +0x50
 *   branch +0x68 -> +0x74
 *   test +0x3c cmp r6, #0
 *   test +0x64 cmp r6, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e6aa0; the literal pool and
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

extern void native_fn_021e63a4(void);
extern void native_fn_021e63c8(void);
extern void native_fn_0202859c(void);
extern void native_fn_020285c8(void);
extern void native_fn_02028280(void);
extern void native_fn_020448f4(void);


asm u32 native_ov000_021e6aa0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    mov r8, r0
    mvn r0, #0
    bl native_fn_021e63a4
    mov r6, r0
    mvn r0, #0
    bl native_fn_021e63c8
    mov r0, r6
    mov r1, #0
    bl native_fn_0202859c
    mov r4, r0
    mov r0, r6
    mov r1, #0
    bl native_fn_020285c8
    mov r5, r0
    cmp r6, #0
    beq ov000_021e6aa0_L50
    mov r0, r6
    bl native_fn_02028280
    mov r7, r0
ov000_021e6aa0_L50:
    mov r0, r8
    mov r1, r4
    mov r2, r5
    bl native_fn_020448f4
    mov r4, r0
    cmp r6, #0
    beq ov000_021e6aa0_L74
    mov r0, r7
    bl native_fn_02028280
ov000_021e6aa0_L74:
    mov r0, r4
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
