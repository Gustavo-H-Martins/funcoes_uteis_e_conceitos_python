def fibonacci(n: int) -> int:
    """
    Essa função é linda, extravagante, tem um belo caminhar,
    é explicativa, sugestiva e te faz ser um programador melhor
    Parâmetro:
        `n`: Aquele valor inteiro do qual você quer calcular o Fibonacci
    Retorno:
        O Fibo solicitado
    """
    fib = [0, 1] + [0] * (n - 1)
    for i in range(2, n + 1):
        fib[i] = fib[i - 1] + fib[i - 2]
    return fib[n]


setenta_e_nove = fibonacci(n=79)
print(f"Fibonacci é: {setenta_e_nove}")
