/* main row 0x02065d4c: 60 bytes.
 *
 * What it does: Resolves an object by id, caches it at block+4 and object+8 at block,
 * and reports success.
 *
 * Decoded shape: 1 call, no loop.
 *
 *   pool +0x34 -> native_data_020de204 (image word 0x020de204)
 *   pool +0x38 -> native_data_021c2ab4 (image word 0x021c2ab4)
 *   call +0x0c -> native_fn_0203cc2c
 *   test +0x14 cmp r0, #0
 *   memory +0x18 str r0, [r1, #4]
 *   memory +0x28 str r0, [r1]
 *   2 store instruction(s)
 *
 * Why transcribed rather than written as C: C if-converts the conditional stores (`strne`/`movne`); the
 * image branches
 * Recorded in docs/authoring/2026-11-11-main-rows-2.md.
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02065d4c; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts
 * the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_020de204[];
extern u8 native_data_021c2ab4[];
extern void native_fn_0203cc2c(void);


asm u32 native_main_02065d4c (register u32 a0)
{
    stmdb sp!, {r3, lr}
    mov r1, r0
    ldr r0, =native_data_020de204
    bl native_fn_0203cc2c
    ldr r1, =native_data_021c2ab4
    cmp r0, #0
    str r0, [r1, #4]
    moveq r0, #0
    ldmeqia sp!, {r3, pc}
    add r0, r0, #8
    str r0, [r1]
    mov r0, #1
    ldmia sp!, {r3, pc}
}
