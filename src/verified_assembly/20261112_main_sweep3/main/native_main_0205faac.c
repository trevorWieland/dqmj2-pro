/* main row 0x0205faac: 60 bytes.
 *
 * What it does: calls 1 helper; 2 loads, 2 stores; 2 branches, 1 backward; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   branch +0x18 -> +0x30
 *   test +0x10 cmp r4, #0
 *   test +0x20 cmp r2, #2
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0205faac; the literal pool and
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

extern void native_fn_0205f98c(void);


asm u32 native_main_0205faac (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r0, [r0, #0x1c]
    mov r4, r2
    bl native_fn_0205f98c
    cmp r4, #0
    ldr r1, [r0, #0x7c]
    beq main_0205faac_L30
    and r2, r1, #2
    cmp r2, #2
    orrne r1, r1, #2
    strne r1, [r0, #0x7c]
    ldmia sp!, {r4, pc}
main_0205faac_L30:
    bic r1, r1, #2
    str r1, [r0, #0x7c]
    ldmia sp!, {r4, pc}
}
