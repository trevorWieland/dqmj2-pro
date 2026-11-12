/* main row 0x020622ec: 60 bytes.
 *
 * What it does: calls 1 helper; 1 branch, 1 backward; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   back edge +0x34 -> +0x18
 *   test +0x10 cmp r6, r5
 *   test +0x2c cmp r5, r0, asr #24
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020622ec; the literal pool and
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

extern void native_fn_02061d08(void);


asm u32 native_main_020622ec (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r6, r0
    mov r5, r1
    mov r4, r2
    cmp r6, r5
    ldmgeia sp!, {r4, r5, r6, pc}
main_020622ec_L18:
    mov r0, r6
    mov r1, r4
    bl native_fn_02061d08
    add r0, r6, #1
    mov r0, r0, lsl #0x18
    cmp r5, r0, asr #24
    mov r6, r0, asr #0x18
    bgt main_020622ec_L18
    ldmia sp!, {r4, r5, r6, pc}
}
