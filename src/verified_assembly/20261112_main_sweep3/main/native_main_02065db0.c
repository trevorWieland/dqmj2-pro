/* main row 0x02065db0: 60 bytes.
 *
 * What it does: calls 3 helpers; 2 loads, 0 stores; 1 branch; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   branch +0x18 -> +0x28
 *   test +0x10 cmp r4, #5
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02065db0; the literal pool and
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

extern void native_fn_0203cfe0(void);
extern void native_fn_02065d88(void);


asm u32 native_main_02065db0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    bl native_fn_0203cfe0
    mov r4, r0
    cmp r4, #5
    mov r0, r5
    bne main_02065db0_L28
    bl native_fn_02065d88
    ldrh r0, [r0, #8]
    ldmia sp!, {r3, r4, r5, pc}
main_02065db0_L28:
    bl native_fn_02065d88
    rsb r1, r4, r4, lsl #3
    add r0, r0, r1
    ldrb r0, [r0, #0x3a]
    ldmia sp!, {r3, r4, r5, pc}
}
