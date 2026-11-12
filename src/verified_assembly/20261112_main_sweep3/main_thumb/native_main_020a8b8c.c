/* main row 0x020a8b8c: 54 bytes.
 *
 * What it does: calls 2 helpers; 2 loads, 2 stores; 2 branches, 1 backward; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   branch +0x08 -> +0x10
 *   back edge +0x1e -> +0x14
 *   test +0x06 cmp r3, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020a8b8c; the literal pool and
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

extern void native_fn_020902f0(void);
extern void native_fn_020a8b4c(void);


asm u32 native_main_020a8b8c (register u32 a0)
{
    push {r3, r4, r5, lr}
    sub sp, #8
    ldrh r3, [r1, #2]
    cmp r3, #0
    bne main_020a8b8c_L10
    add sp, #8
    mov r0, #0
    pop {r3, r4, r5, pc}
main_020a8b8c_L10:
    add r5, sp, #0
    mov r4, #8
main_020a8b8c_L14:
    ldrb r3, [r1, #0]
    add r1, r1, #1
    strb r3, [r5, #0]
    add r5, r5, #1
    sub r4, r4, #1
    bne main_020a8b8c_L14
    add r1, sp, #0
    strb r2, [r1, #0]
    add r1, sp, #0
    bl native_fn_020902f0
    mov r1, #0
    mvn r1, r1
    bl native_fn_020a8b4c
    add sp, #8
    pop {r3, r4, r5, pc}
}
