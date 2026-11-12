/* ov001 row 0x0220619c: 88 bytes.
 *
 * What it does: 22 instructions; 6 call(s) to 0x0205e7a8, 0x02212868, 0x0205eb00, +3 more; loops (back edge at +0x0c); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: loop with 6 calls (22 instructions, 6 calls, 2 branches, 3 back edges, 0 literal slots).
 *
 *   branch +0x28 -> +0x44
 *   branch +0x34 -> +0x44
 *   test +0x20 cmp r4, r1
 *   test +0x24 cmpne r4, r5
 *   test +0x30 cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220619c; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_0205e7a8(void);
extern void native_fn_02212868(void);
extern void native_fn_0205eb00(void);
extern void native_fn_0205f210(void);
extern void native_fn_02212838(void);
extern void native_fn_02212818(void);


asm u32 native_ov001_0220619c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mvn r0, #0
    mov r1, #60
    bl native_fn_0205e7a8
    mov r5, r0
    bl native_fn_02212868
    mov r4, r0
    mvn r1, #0
    cmp r4, r1
    cmpne r4, r5
    beq ov001_0220619c_L44
    bl native_fn_0205eb00
    cmp r0, #0
    beq ov001_0220619c_L44
    mov r0, r4
    mov r1, #1
    bl native_fn_0205f210
ov001_0220619c_L44:
    mov r0, r5
    bl native_fn_02212838
    mov r0, #0
    bl native_fn_02212818
    ldmia sp!, {r3, r4, r5, pc}
}
