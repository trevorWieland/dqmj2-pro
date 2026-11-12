/* main row 0x020a5fe4: 54 bytes.
 *
 * What it does: calls 2 helpers; 2 loads, 1 store; 3 branches; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   branch +0x08 -> +0x10
 *   branch +0x1c -> +0x2a
 *   branch +0x28 -> +0x30
 *   test +0x06 cmp r0, #0
 *   test +0x1a cmp r0, #0
 *   test +0x26 cmp r0, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020a5fe4; the literal pool and
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

extern void native_fn_020a8a3c(void);
extern void native_fn_0201d69c(void);


asm u32 native_main_020a5fe4 (register u32 a0)
{
    push {r3, r4, r5, lr}
    sub sp, #8
    add r5, r2, #0
    cmp r0, #0
    bne main_020a5fe4_L10
    add sp, #8
    mov r0, #0
    pop {r3, r4, r5, pc}
main_020a5fe4_L10:
    str r1, [sp]
    ldr r0, [r0, #0x18]
    add r1, sp, #0
    bl native_fn_020a8a3c
    cmp r0, #0
    beq main_020a5fe4_L2a
    ldr r4, [r0, #4]
    add r0, r4, #0
    blx native_fn_0201d69c
    cmp r0, #0
    bne main_020a5fe4_L30
main_020a5fe4_L2a:
    add sp, #8
    add r0, r5, #0
    pop {r3, r4, r5, pc}
main_020a5fe4_L30:
    add r0, r4, #0
    add sp, #8
    pop {r3, r4, r5, pc}
}
