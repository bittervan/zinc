static long global_value = 11;

int main(void) {
    long values[3];
    values[0] = global_value;
    values[1] = 22;
    values[2] = values[0] + values[1];
    global_value = values[2] + 5;
    return (int)global_value;
}
