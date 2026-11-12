/* main row 0x0208baac: 52 bytes.
 *
 * What it does: calls 4 helpers; 4 loads, 3 stores; 3 local pool words (0x021cfea0, 0x021cff60, 0x021cfcf8); falls through
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x28 -> constant 0x021cfea0 (image word 0x021cfea0)
 *   pool +0x2c -> constant 0x021cff60 (image word 0x021cff60)
 *   pool +0x30 -> constant 0x021cfcf8 (image word 0x021cfcf8)
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0208baac; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the field meanings and the callee contracts are not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_0208ba68(void);
extern void native_fn_02006890(void);
extern void native_fn_020067fc(void);
extern void native_fn_0208b840(void);


asm u32 native_main_0208baac (register u32 a0)
{
    push {r3, lr}
    bl native_fn_0208ba68
    ldr r0, =0x021cfea0
    blx native_fn_02006890
    ldr r0, =0x021cff60
    blx native_fn_020067fc
    ldr r1, =0x021cfcf8
    mov r0, #0
    str r0, [r1, #0x54]
    bl native_fn_0208b840
    ldr r0, =0x021cfcf8
    mov r1, #0
    str r1, [r0, #0x58]
    str r1, [r0, #0x5c]
    pop {r3, pc}
    mov r8, r8
}
