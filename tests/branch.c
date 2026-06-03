int main(void) {
    int score = 0;
    volatile int input = -3;
    int a = input;
    unsigned int b = (unsigned int)(input + 10);

    if (a < 0) {
        score += 1;
    }

    if (b >= 7U) {
        score += 2;
    }

    if (a != (int)b) {
        score += 4;
    }

    if (score == 7) {
        score += 8;
    }

    return score;
}
