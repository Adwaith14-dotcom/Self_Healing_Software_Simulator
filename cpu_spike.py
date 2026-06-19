def heavy_computation():
    while True:
        result = [i**2 for i in range(1000000)]
        heavy_computation()
