typedef unsigned char u8;
extern u8 native_battle_skill_blocks[][10];
u8 *saved_battle_skill_pointer(int index) {
    return native_battle_skill_blocks[index];
}
