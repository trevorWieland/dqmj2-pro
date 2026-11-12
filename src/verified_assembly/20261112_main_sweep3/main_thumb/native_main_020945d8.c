/* main row 0x020945d8: 40 bytes.
 *
 * What it does: calls 1 helper; 1 indirect call through a register; 2 loads, 1 store; 1 branch; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   branch +0x14 -> +0x24
 *   test +0x12 tst r1, r5
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020945d8; the literal pool and
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

extern void native_fn_020946ec(void);


asm u32 native_main_020945d8 (register u32 a0)
{
    push {r3, r4, r5, lr}
    add r5, r0, #0
    mov r0, #1
    add r4, r1, #0
    bl native_fn_020946ec
    add r2, r0, #0
    ldrb r0, [r2, #8]
    add r1, r0, #0
    tst r1, r5
    bne main_020945d8_L24
    orr r0, r5
    strb r0, [r2, #8]
    ldr r2, [r2, #0]
    add r0, r5, #0
    add r1, r4, #0
    blx r2
    pop {r3, r4, r5, pc}
main_020945d8_L24:
    mov r0, #0
    pop {r3, r4, r5, pc}
}
