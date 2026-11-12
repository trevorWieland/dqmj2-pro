/* main row 0x02028dec: 56 bytes.
 *
 * What it does: calls 1 helper; 1 indirect call through a register; 2 loads, 0 stores; 1 local pool word (0x020edd0c); 2 branches; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x34 -> constant 0x020edd0c (image word 0x020edd0c)
 *   branch +0x0c -> +0x2c
 *   branch +0x18 -> +0x2c
 *   test +0x04 cmp r0, #0
 *   test +0x14 cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02028dec; the literal pool and
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

extern void native_fn_0202e858(void);


asm u32 native_main_02028dec (register u32 a0)
{
    stmdb sp!, {r4, lr}
    cmp r0, #0
    mov r4, #0
    beq main_02028dec_L2c
    bl native_fn_0202e858
    cmp r0, #0
    beq main_02028dec_L2c
    ldr r1, =0x020edd0c
    ldr r1, [r1, #4]
    blx r1
    mov r4, r0
main_02028dec_L2c:
    mov r0, r4
    ldmia sp!, {r4, pc}
}
