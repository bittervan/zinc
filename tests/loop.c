int main(void) {
    volatile int limit = 8;
    int sum = 0;
    for (int i = 1; i <= limit; ++i) {
        sum += i;
    }
    return sum;
}
