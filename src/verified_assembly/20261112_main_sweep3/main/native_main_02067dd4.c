/* main row 0x02067dd4: 64 bytes.
 *
 * What it does: Sums 0x02067e54(0x02062a50(i)) for i in [0, 0x02062aa0()) and returns the total.
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   branch +0x18 -> +0x38
 *   back edge +0x34 -> +0x1c
 *   test +0x10 cmp r6, #0
 *   test +0x2c cmp r4, r6
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02067dd4; the literal pool and
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

extern void native_fn_02062aa0(void);
extern void native_fn_02062a50(void);
extern void native_fn_02067e54(void);


asm u32 native_main_02067dd4 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r5, #0
    bl native_fn_02062aa0
    mov r6, r0
    cmp r6, #0
    mov r4, r5
    ble main_02067dd4_L38
main_02067dd4_L1c:
    mov r0, r4
    bl native_fn_02062a50
    bl native_fn_02067e54
    add r4, r4, #1
    cmp r4, r6
    add r5, r5, r0
    blt main_02067dd4_L1c
main_02067dd4_L38:
    mov r0, r5
    ldmia sp!, {r4, r5, r6, pc}
}
