/* main row 0x020a8c34: 52 bytes.
 *
 * What it does: calls 2 helpers; 3 loads, 3 stores; 1 branch, 1 backward; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   back edge +0x16 -> +0x0c
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020a8c34; the literal pool and
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

extern void native_fn_020903f8(void);
extern void native_fn_020a8b4c(void);


asm u32 native_main_020a8c34 (register u32 a0)
{
    push {r4, r5, r6, r7, lr}
    sub sp, #0xc
    ldr r5, [sp, #0x20]
    add r7, r3, #0
    add r6, sp, #4
    mov r4, #8
main_020a8c34_Lc:
    ldrb r3, [r5, #0]
    add r5, r5, #1
    strb r3, [r6, #0]
    add r6, r6, #1
    sub r4, r4, #1
    bne main_020a8c34_Lc
    ldr r4, [sp, #0x24]
    add r3, sp, #4
    strb r4, [r3, #0]
    add r3, sp, #4
    str r3, [sp]
    add r3, r7, #0
    bl native_fn_020903f8
    mov r1, #0
    mvn r1, r1
    bl native_fn_020a8b4c
    add sp, #0xc
    pop {r4, r5, r6, r7, pc}
}
