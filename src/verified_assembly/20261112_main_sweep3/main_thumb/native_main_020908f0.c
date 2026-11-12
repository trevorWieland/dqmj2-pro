/* main row 0x020908f0: 40 bytes.
 *
 * What it does: calls 2 helpers; 1 load, 1 store; 1 local pool word (0x02090919); 1 branch; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x24 -> native_fn_02090918+1 (image word 0x02090919)
 *   branch +0x12 -> +0x1a
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020908f0; the literal pool and
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

extern void native_fn_02090918(void);
extern void native_fn_0208ebd8(void);
extern void native_fn_0208eca4(void);


asm u32 native_main_020908f0 (register u32 a0)
{
    push {r3, r4, r5, lr}
    add r5, r0, #0
    add r4, r1, #0
    ldr r0, =native_fn_02090918+1
    add r1, r5, #0
    mov r2, #1
    bl native_fn_0208ebd8
    add r1, r0, #0
    bne main_020908f0_L1a
    mov r0, #0x20
    mvn r0, r0
    pop {r3, r4, r5, pc}
main_020908f0_L1a:
    add r0, r5, #0
    str r4, [r1, #0x10]
    bl native_fn_0208eca4
    pop {r3, r4, r5, pc}
}
