/* main row 0x0204514c: 64 bytes.
 *
 * What it does: calls 2 helpers; 3 loads, 0 stores; 2 branches; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   branch +0x0c -> +0x14
 *   branch +0x1c -> +0x24
 *   test +0x18 cmp r0, r4
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0204514c; the literal pool and
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

extern void native_fn_02008430(void);


asm u32 native_main_0204514c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    movs r5, r0
    mov r4, r1
    bne main_0204514c_L14
    bl native_fn_02008430
main_0204514c_L14:
    ldr r0, [r5]
    cmp r0, r4
    bhi main_0204514c_L24
    bl native_fn_02008430
main_0204514c_L24:
    mov r0, r4, lsl #2
    add r0, r0, #4
    add r1, r5, r0
    ldr r1, [r1, #4]
    ldr r0, [r5, r0]
    sub r0, r1, r0
    ldmia sp!, {r3, r4, r5, pc}
}
