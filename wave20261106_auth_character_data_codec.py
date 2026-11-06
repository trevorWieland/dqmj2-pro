import re
from wave20261106_gp_character_data_codec import encode,literal


def render(document,symbol):
    if not re.fullmatch(r'native_auth_character_[0-9a-f]{8}',symbol):raise ValueError('Exact Auth typed character symbol differs')
    payload,expression=encode(document)
    return '#include "characters.h"\nconst char '+symbol+'[] = '+expression+';\n',payload


def header(assets):
    declarations=[f"extern const char {row['nativeSymbol']}[{row['bytes']}];"for row in assets]
    return '\n'.join(['#ifndef AUTH_CHARACTER_OBJECTS_H','#define AUTH_CHARACTER_OBJECTS_H','typedef char AuthCharacterWidthMustBeOne[(sizeof(char)==1)?1:-1];',*declarations,'#endif',''])
