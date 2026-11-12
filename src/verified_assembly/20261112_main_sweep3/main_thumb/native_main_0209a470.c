/* main row 0x0209a470: 48 bytes.
 *
 * What it does: calls 1 helper; 5 loads, 4 stores; 1 local pool word (0x027ffe0f); 2 branches; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x2c -> constant 0x027ffe0f (image word 0x027ffe0f)
 *   branch +0x08 -> +0x0e
 *   branch +0x0c -> +0x14
 *   test +0x06 cmp r4, #0x80
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0209a470; the literal pool and
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

extern void native_fn_0209a1a8(void);


asm u32 native_main_0209a470 (register u32 a0)
{
    push {r3, r4, r5, lr}
    sub sp, #0x10
    ldr r4, [sp, #0x28]
    cmp r4, #0x80
    bne main_0209a470_Le
    mov r5, #0x41
    b main_0209a470_L14
main_0209a470_Le:
    ldr r5, =0x027ffe0f
    mov r4, #0
    ldrsb r5, [r5, r4]
main_0209a470_L14:
    add r4, sp, #0xc
    strb r5, [r4, #0]
    ldr r4, [sp, #0x20]
    str r4, [sp]
    ldr r4, [sp, #0x24]
    str r4, [sp, #4]
    add r4, sp, #0xc
    str r4, [sp, #8]
    bl native_fn_0209a1a8
    add sp, #0x10
    pop {r3, r4, r5, pc}
}
