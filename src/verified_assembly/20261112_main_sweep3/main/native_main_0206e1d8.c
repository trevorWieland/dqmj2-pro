/* main row 0x0206e1d8: 60 bytes.
 *
 * What it does: calls 2 helpers; 2 loads, 0 stores; 2 branches, 1 backward; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   branch +0x18 -> +0x24
 *   back edge +0x34 -> +0x08
 *   test +0x14 cmp r0, #0
 *   test +0x30 cmp r4, #6
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0206e1d8; the literal pool and
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

extern void native_fn_02061dcc(void);
extern void native_fn_02049ffc(void);


asm u32 native_main_0206e1d8 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, #0
main_0206e1d8_L8:
    mov r0, r4
    bl native_fn_02061dcc
    ldr r0, [r0]
    cmp r0, #0
    beq main_0206e1d8_L24
    ldr r0, [r0, #4]
    bl native_fn_02049ffc
main_0206e1d8_L24:
    add r0, r4, #1
    mov r0, r0, lsl #0x18
    mov r4, r0, asr #0x18
    cmp r4, #6
    blt main_0206e1d8_L8
    ldmia sp!, {r4, pc}
}
