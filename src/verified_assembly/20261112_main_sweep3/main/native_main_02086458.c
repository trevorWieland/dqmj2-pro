/* main row 0x02086458: 60 bytes.
 *
 * What it does: calls 1 helper; 5 loads, 2 stores; 1 branch; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   branch +0x10 -> +0x2c
 *   test +0x0c cmp r2, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02086458; the literal pool and
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

extern void native_fn_02084f9c(void);


asm u32 native_main_02086458 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    mov r1, r0
    ldr r2, [r1, #0x20]
    cmp r2, #0
    beq main_02086458_L2c
    ldr r0, [r1, #0x24]
    str r0, [r2]
    ldr r2, [r1, #4]
    ldr r0, [r2, #0x18]
    orr r0, r0, #0x10
    str r0, [r2, #0x18]
main_02086458_L2c:
    ldrb r0, [r1, #0x2e]
    bl native_fn_02084f9c
    mov r0, #1
    ldmia sp!, {r3, pc}
}
