/* main row 0x0203a090: 52 bytes.
 *
 * What it does: calls 1 helper; 4 loads, 0 stores; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   test +0x08 cmp r1, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0203a090; the literal pool and
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

extern void native_fn_020260dc(void);


asm u32 native_main_0203a090 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r1, [r0]
    cmp r1, #0
    moveq r0, #0
    ldmeqia sp!, {r3, pc}
    ldr r1, [r0]
    mov r0, #0x3e8
    ldr r3, [r1, #0x160]
    ldrh r2, [r1, #0xc4]
    umull r0, r1, r3, r0
    mov r3, #0
    bl native_fn_020260dc
    ldmia sp!, {r3, pc}
}
