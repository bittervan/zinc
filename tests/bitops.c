int main(void) {
    volatile unsigned long seed = 0x55aa00ffUL;
    unsigned long a = seed;
    unsigned long b = seed >> 3;
    unsigned long x = (a & b) ^ (a | b);
    unsigned long y = (x << 3) ^ (x >> 5);
    long z = -16;
    return (int)(y ^ (unsigned long)(z >> 2));
}
