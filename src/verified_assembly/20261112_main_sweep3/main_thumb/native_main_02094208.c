/* main row 0x02094208: 56 bytes.
 *
 * What it does: calls 1 helper; 3 loads, 2 stores; 3 branches, 1 backward; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   branch +0x16 -> +0x2e
 *   back edge +0x2c -> +0x18
 *   branch +0x30 -> +0x36
 *   test +0x14 cmp r6, #1
 *   test +0x2a cmp r6, #1
 *   test +0x2e cmp r6, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02094208; the literal pool and
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

extern void native_fn_02008d78(void);


asm u32 native_main_02094208 (register u32 a0)
{
    push {r4, r5, r6, lr}
    add r4, r1, #0
    add r6, r2, #0
    mov r1, #0
    lsl r2, r3, #1
    add r5, r0, #0
    blx native_fn_02008d78
    sub r0, r6, #1
    add r4, r4, r0
    cmp r6, #1
    ble main_02094208_L2e
main_02094208_L18:
    sub r0, r4, #1
    ldrb r0, [r0, #0]
    ldrb r1, [r4, #0]
    sub r6, r6, #2
    lsl r0, r0, #8
    add r0, r1, r0
    strh r0, [r5, #0]
    add r5, r5, #2
    sub r4, r4, #2
    cmp r6, #1
    bgt main_02094208_L18
main_02094208_L2e:
    cmp r6, #0
    ble main_02094208_L36
    ldrb r0, [r4, #0]
    strh r0, [r5, #0]
main_02094208_L36:
    pop {r4, r5, r6, pc}
}
