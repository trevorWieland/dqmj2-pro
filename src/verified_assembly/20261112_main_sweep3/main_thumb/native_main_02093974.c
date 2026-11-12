/* main row 0x02093974: 36 bytes.
 *
 * What it does: calls 1 helper; 1 load, 1 store; 2 branches, 1 backward; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   branch +0x08 -> +0x1a
 *   back edge +0x18 -> +0x0c
 *   test +0x06 cmp r3, #0
 *   test +0x16 cmp r2, r3
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02093974; the literal pool and
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

extern void native_fn_02093930(void);


asm u32 native_main_02093974 (register u32 a0)
{
    push {r4, lr}
    add r3, r1, #0
    mov r2, #0
    cmp r3, #0
    ble main_02093974_L1a
    add r4, r0, #0
main_02093974_Lc:
    ldrh r1, [r4, #0]
    add r2, r2, #1
    mvn r1, r1
    strh r1, [r4, #0]
    add r4, r4, #2
    cmp r2, r3
    blt main_02093974_Lc
main_02093974_L1a:
    add r1, r0, #0
    mov r2, #1
    bl native_fn_02093930
    pop {r4, pc}
}
