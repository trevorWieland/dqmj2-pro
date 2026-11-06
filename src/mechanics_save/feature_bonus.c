typedef unsigned char u8;
extern int saved_feature_occurrences(int, const u8 *);
int saved_record_feature_bonus24(const u8 *features) {
    int value = 0;
    value += saved_feature_occurrences(128, features) * 5;
    value += saved_feature_occurrences(129, features) * 10;
    value += saved_feature_occurrences(130, features) * 15;
    value += saved_feature_occurrences(131, features) * 20;
    value += saved_feature_occurrences(132, features) * 22;
    value += saved_feature_occurrences(133, features) * 24;
    value += saved_feature_occurrences(134, features) * 26;
    value += saved_feature_occurrences(135, features) * 28;
    value += saved_feature_occurrences(136, features) * 30;
    return 35 * saved_feature_occurrences(137, features) + value;
}
int saved_record_feature_bonus26(const u8 *features) {
    int value = 0;
    value += saved_feature_occurrences(138, features) * 5;
    value += saved_feature_occurrences(139, features) * 10;
    value += saved_feature_occurrences(140, features) * 15;
    value += saved_feature_occurrences(141, features) * 20;
    value += saved_feature_occurrences(142, features) * 22;
    value += saved_feature_occurrences(143, features) * 24;
    value += saved_feature_occurrences(144, features) * 26;
    value += saved_feature_occurrences(145, features) * 28;
    value += saved_feature_occurrences(146, features) * 30;
    return 35 * saved_feature_occurrences(147, features) + value;
}
